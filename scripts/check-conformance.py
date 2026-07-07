#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""check-conformance.py — independent validation of the SemVer-Trust conformance vectors.

Validates ``conformance/levels.json`` and ``conformance/precedence.json`` against a
second, independent implementation of the spec rules they encode
(``spec/semver-trust.md`` §3.2-§3.3, §4.1-§4.2, §7.1-§7.2). This is deliberately NOT
the reference Go implementation, and it shares no code with
``scripts/check-drift.py`` — the SemVer comparator and the level invariant are
re-implemented here from first principles. Agreement between two independent
implementations is the point.

    python3 scripts/check-conformance.py

Exit code 0 = all vectors valid. Requires Python 3.11+, stdlib only.
"""

import json
import re
import sys
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFORMANCE = ROOT / "conformance"
LEVELS = CONFORMANCE / "levels.json"
PRECEDENCE = CONFORMANCE / "precedence.json"
SPEC = ROOT / "spec" / "semver-trust.md"

AUTHORSHIP = ("agent", "mixed", "ambiguous", "human")
REVIEW = ("none", "agent_independent", "human_distinct")

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'}  {name}{('  — ' + detail) if (detail and not ok) else ''}")
    if not ok:
        failures.append(name)


# ---- Independent spec implementations --------------------------------------
#
# level = f(accountable-human count, agent corroboration), per §3.2 / Appendix B.
# Humans: the author (if human) plus a *distinct* human reviewer. Agent
# corroboration (independent agent review, §3.3) lifts the zero-human case T0->T1.
def invariant_level(authorship: str, review: str) -> str:
    humans = (authorship == "human") + (review == "human_distinct")
    if humans == 0:
        return "T1" if review == "agent_independent" else "T0"
    if humans == 1:
        return "T2"
    return "T3"


# SemVer 2.0.0 §11 precedence via a total-order sort key. A release outranks any
# pre-release of the same core; numeric identifiers sort below alphanumeric ones;
# a shorter run of equal-prefixed identifiers sorts lower.
_SEMVER = re.compile(
    r"^(?P<major>0|[1-9][0-9]*)\.(?P<minor>0|[1-9][0-9]*)\.(?P<patch>0|[1-9][0-9]*)"
    r"(?:-(?P<pre>[0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$"
)


def precedence_key(version: str) -> tuple:
    m = _SEMVER.match(version)
    if not m:
        raise ValueError(f"not a SemVer version: {version}")
    core = (int(m["major"]), int(m["minor"]), int(m["patch"]))
    pre = m["pre"]
    if not pre:
        return (core, (1,))  # release ranks above any pre-release
    identifiers = []
    for token in pre.split("."):
        if token.isdigit():
            identifiers.append((0, int(token), ""))  # numeric < alphanumeric
        else:
            identifiers.append((1, -1, token))  # ASCII-lexical
    return (core, (0, tuple(identifiers)))


# §7.1 ABNF, exactly: the strict trust-tag grammar (clean core-version OR
# trust-version), and a general SemVer-tag grammar used to tell a plain
# pre-release version (accepted, trust absent) from a rejected malformed tag.
_TRUST_TAG = re.compile(
    r"^(?:(?P<path>[0-9A-Za-z._-]+(?:/[0-9A-Za-z._-]+)*)/)?"
    r"v(?P<core>(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))"
    r"(?:-t(?P<level>[0-3])\.(?P<iter>[1-9][0-9]*))?$"
)
_SEMVER_TAG = re.compile(
    r"^(?:(?P<path>[0-9A-Za-z._-]+(?:/[0-9A-Za-z._-]+)*)/)?"
    r"v(?P<core>(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))"
    r"(?:-(?P<pre>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z.-]+)?$"
)


# ---- Checks ----------------------------------------------------------------
def check_structure(docs: dict[str, dict]) -> None:
    ids: list[str] = []
    versions = []
    for doc in docs.values():
        versions.append(doc.get("spec_version"))
        for vec in doc.get("vectors", []):
            ids.append(vec.get("id"))
            spec = vec.get("spec")
            check(
                f"vector-spec-ref-{vec.get('id')}",
                isinstance(spec, str) and spec.strip() != "",
                "empty spec reference",
            )
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    check("vector-ids-unique", not duplicates, f"duplicate ids: {duplicates}")
    check("vector-ids-nonempty", all(isinstance(i, str) and i for i in ids))
    check(
        "spec-version-consistent",
        len(set(versions)) == 1 and bool(versions[0]),
        f"spec_version differs across files: {versions}",
    )


def check_spec_version_matches_spec(version: str) -> None:
    if not SPEC.exists():
        print(f"PASS  spec-version-matches-spec  (skipped: {SPEC.name} not in this checkout)")
        return
    m = re.search(r"\*\*Draft v(?P<v>[0-9]+\.[0-9]+)\*\*", SPEC.read_text(encoding="utf-8"))
    check(
        "spec-version-matches-spec",
        m is not None and m["v"] == version,
        f"vectors pin {version} but spec header is {m['v'] if m else 'unknown'}",
    )


def check_levels(vectors: list[dict]) -> None:
    matrix = [v for v in vectors if v.get("kind") == "matrix"]
    classify = [v for v in vectors if v.get("kind") == "classify"]
    check("levels-matrix-nonempty", bool(matrix))
    check("levels-classify-nonempty", bool(classify))

    for vec in matrix:
        author, review = vec["inputs"]["authorship"], vec["inputs"]["review"]
        want = invariant_level(author, review)
        check(
            f"levels-invariant-{vec['id']}",
            vec["expected"]["level"] == want,
            f"{author}/{review}: invariant says {want}, vector says {vec['expected']['level']}",
        )

    for vec in classify:
        author, review = vec["expected"]["authorship"], vec["expected"]["review"]
        want = invariant_level(author, review)
        check(
            f"levels-invariant-{vec['id']}",
            vec["expected"]["level"] == want,
            f"{author}/{review}: invariant says {want}, vector says {vec['expected']['level']}",
        )

    present = {(v["inputs"]["authorship"], v["inputs"]["review"]) for v in matrix}
    missing = [f"{a}/{r}" for a in AUTHORSHIP for r in REVIEW if (a, r) not in present]
    check("levels-matrix-exhaustive", not missing, f"missing combos: {missing}")
    check(
        "levels-matrix-self-review",
        ("human", "human_same_identity") in present,
        "missing the human/human_same_identity self-review vector",
    )


def check_precedence(vectors: list[dict]) -> None:
    prec = [v for v in vectors if v.get("kind") == "precedence"]
    check("precedence-group-nonempty", bool(prec))
    for vec in prec:
        ordered = vec.get("ordered", [])
        try:
            keys = [precedence_key(s) for s in ordered]
        except ValueError as exc:
            check(f"precedence-{vec['id']}", False, str(exc))
            continue
        ascending = len(ordered) >= 2 and all(a < b for a, b in pairwise(keys))
        check(f"precedence-{vec['id']}", ascending, f"not strictly ascending: {ordered}")


def _check_trust_version(vec: dict, tag: str, exp: dict) -> None:
    m = _TRUST_TAG.match(tag)
    ok = m is not None
    if m is not None:
        level = int(m["level"]) if m["level"] is not None else None
        iteration = int(m["iter"]) if m["iter"] is not None else None
        ok = (
            m["path"] == exp["component_path"]
            and m["core"] == exp["core"]
            and level == exp["level"]
            and iteration == exp["iteration"]
        )
    check(f"grammar-{vec['id']}", ok, f"trust-version parse mismatch for {tag}")


def _check_plain_version(vec: dict, tag: str, exp: dict) -> None:
    sm = _SEMVER_TAG.match(tag)
    pre = sm["pre"] if sm else None
    ok = (
        _TRUST_TAG.match(tag) is None
        and sm is not None
        and pre is not None
        and re.match(r"t[0-9]", pre) is None
        and sm["path"] == exp["component_path"]
        and sm["core"] == exp["core"]
        and pre == exp["prerelease"]
        and exp["level"] is None
        and exp["iteration"] is None
    )
    check(f"grammar-{vec['id']}", ok, f"plain-version parse mismatch for {tag}")


def _check_invalid(vec: dict, tag: str, exp: dict) -> None:
    reason = exp.get("reason")
    ok = _TRUST_TAG.match(tag) is None and isinstance(reason, str) and reason != ""
    check(f"grammar-{vec['id']}", ok, f"strict grammar accepted a tag marked invalid: {tag}")


def check_grammar(vectors: list[dict]) -> None:
    gram = [v for v in vectors if v.get("kind") == "grammar"]
    check("grammar-group-nonempty", bool(gram))
    handlers = {
        "trust_version": _check_trust_version,
        "plain_version": _check_plain_version,
        "invalid": _check_invalid,
    }
    for vec in gram:
        exp = vec["expected"]
        handler = handlers.get(exp["outcome"])
        if handler is None:
            check(f"grammar-{vec['id']}", False, f"unknown outcome {exp['outcome']!r}")
            continue
        handler(vec, vec["tag"], exp)


def main() -> int:
    docs: dict[str, dict] = {}
    for path in (LEVELS, PRECEDENCE):
        if not path.exists():
            check(f"file-exists-{path.name}", False, str(path))
            continue
        try:
            docs[path.name] = json.loads(path.read_text(encoding="utf-8"))
            check(f"json-wellformed-{path.name}", True)
        except json.JSONDecodeError as exc:
            check(f"json-wellformed-{path.name}", False, str(exc))

    if len(docs) == 2:
        check_structure(docs)
        check_spec_version_matches_spec(docs[LEVELS.name]["spec_version"])
        check_levels(docs[LEVELS.name]["vectors"])
        check_precedence(docs[PRECEDENCE.name]["vectors"])
        check_grammar(docs[PRECEDENCE.name]["vectors"])

    print(
        f"\n{'OK' if not failures else 'CONFORMANCE VECTORS INVALID'}: "
        f"{len(failures)} failure(s)" + (f" -> {failures}" if failures else "")
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

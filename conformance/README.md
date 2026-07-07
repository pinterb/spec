<!-- SPDX-License-Identifier: Apache-2.0 -->
# SemVer-Trust Conformance Vectors

These vectors are the **sync contract** between the [SemVer-Trust specification](../spec/semver-trust.md)
and every implementation of it. They are data, not prose: a conformance harness loads them, exercises the
implementation under test, and asserts the implementation reproduces the encoded expectations. The Go
reference implementation treats them as acceptance tests, and any other implementation claims conformance by
passing them.

Each vector is derived directly from a normative section of the spec and carries a `spec` back-reference to
it. The vectors in this directory cover **level assignment** (§3.2, §3.3, §4.1–§4.2) and **version precedence
and tag grammar** (§7.1, §7.2). Aggregation, propagation, and release-decision vectors are added separately.

## File inventory

| Path | Role | License |
|---|---|---|
| `levels.json` | Per-commit trust level assignment vectors (matrix + classification) | Apache 2.0 |
| `precedence.json` | SemVer precedence ordering vectors + §7.1 tag-grammar vectors | Apache 2.0 |
| `check-conformance.py` (in `../scripts/`) | Independent validator for these files (self-check, not the harness) | Apache 2.0 |
| `LICENSE` | Verbatim Apache 2.0 text, vendored so copies carry their license | Apache 2.0 |

`../scripts/check-conformance.py` is a *self-consistency* check: it re-implements the spec rules a second
time (independently of both the reference implementation and `check-drift.py`) and confirms the vectors agree
with that implementation. It is not the conformance harness — a harness runs the *implementation under test*
against these vectors.

## `spec_version` pinning

Every vector file carries a top-level `spec_version` (currently `"0.2"`). It names the spec draft the vectors
encode, not the version of the vector set. The rules:

- The vectors track the pinned spec draft. When they say `"0.2"`, their expectations are those of
  `spec/semver-trust.md` **Draft v0.2**.
- All vector files in this directory MUST share the same `spec_version`; the validator enforces this and
  cross-checks it against the spec's draft header.
- An implementation claims conformance **against a `spec_version`** — "conforms to SemVer-Trust 0.2 level and
  precedence vectors" is the precise claim.

## Vector format

Both files share an envelope:

```json
{
  "$comment": "SPDX-License-Identifier: Apache-2.0",
  "spec_version": "0.2",
  "description": "…what this file covers…",
  "vectors": [ /* … */ ]
}
```

Every vector, regardless of file, has these common fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable, unique identifier, e.g. `levels/matrix/agent-none`. Never reused or repurposed. |
| `kind` | string | Selects the consumption rule: `matrix`, `classify`, `precedence`, or `grammar`. |
| `description` | string | Human-readable intent; editorial, not asserted. |
| `spec` | string | Back-reference to the governing spec section, e.g. `§3.2`. Never empty. |

### `levels.json` — `kind: "matrix"`

Already-classified authorship and review classes mapped to a level. Tests the level function in isolation.

| Field | Type | Values |
|---|---|---|
| `inputs.authorship` | string | `agent`, `mixed`, `ambiguous`, `human` |
| `inputs.review` | string | `none`, `agent_independent`, `human_distinct`, `human_same_identity` |
| `expected.level` | string | `T0`, `T1`, `T2`, `T3` |

`human_same_identity` is self-review, which does not count as review (§3.2 note 2); it appears only on the
`human` authorship row. The matrix group covers every `authorship × review` combination exhaustively.

### `levels.json` — `kind: "classify"`

Raw commit facts mapped to the derived classes **and** the level. Tests the classifier plus the level
function end to end.

| Field | Type | Meaning |
|---|---|---|
| `inputs.signer_identity_class` | string | `human` or `agent` — the verified signer's identity class (§4.2). |
| `inputs.trailers` | object | Git trailers. `Provenance` is `human`/`agent`/`mixed`; `Co-authored-by` is a list of unsigned co-authors. |
| `inputs.policy` | object | `{ "trailers_require": bool }` — whether policy mandates provenance trailers (§4.1). |
| `inputs.review` | object or null | Review facts, or `null` when there is no review. |
| `inputs.review.reviewer_identity_class` | string | `human` or `agent`. |
| `inputs.review.reviewer_identity` | string | The reviewer's identity. |
| `inputs.review.author_identity` | string | The author's identity, for the distinct-identity test (§3.3(2), §3.2 note 2). |
| `inputs.review.separate_context` | bool | Whether the reviewer ran with no shared state (§3.3(1)). |
| `inputs.review.signed_attestation` | bool | Whether a signed review attestation exists (§3.3(3)). |
| `expected.authorship` | string | Derived authorship class. |
| `expected.review` | string | Derived review class (a non-qualifying review classifies as `none`). |
| `expected.level` | string | Resulting level, consistent with `expected.authorship` and `expected.review`. |

### `precedence.json` — `kind: "precedence"`

| Field | Type | Meaning |
|---|---|---|
| `ordered` | array of string | Version strings in **strictly increasing** precedence order (no ties). |
| `note` | string | Why the ordering holds; editorial. |

### `precedence.json` — `kind: "grammar"`

| Field | Type | Meaning |
|---|---|---|
| `tag` | string | The tag string to parse. |
| `expected.outcome` | string | `trust_version`, `plain_version`, or `invalid`. |
| `expected.component_path` | string or null | Extracted path prefix (e.g. `pkg/common`), or `null`. |
| `expected.core` | string or null | Extracted `MAJOR.MINOR.PATCH`, or `null` for `invalid`. |
| `expected.level` | int or null | Trust level `0`–`3`, or `null` when there is no trust suffix. |
| `expected.iteration` | int or null | Iteration (≥ 1), or `null` when there is no trust suffix. |
| `expected.prerelease` | string or null | For `plain_version`, the non-trust pre-release (e.g. `rc.1`); otherwise `null`. |
| `expected.reason` | string or null | For `invalid`, why the tag is rejected; otherwise `null`. |

The three grammar outcomes are distinct on purpose:

- **`trust_version`** — matches the §7.1 grammar: either a clean `[path/]vMAJOR.MINOR.PATCH` or a trust
  suffix `-tLEVEL.ITERATION`. Trust components are extracted.
- **`plain_version`** — a valid SemVer version whose pre-release is not trust-shaped (e.g. `rc.1`). It is
  accepted as an ordinary pre-release with the trust suffix **absent**, not rejected. This keeps
  non-trust tags (rc/alpha/beta) usable while the trust layer simply reports "no trust information".
- **`invalid`** — a *trust-shaped* pre-release (begins with `t` then a digit) that violates the trust
  grammar (two-digit level, missing/zero iteration, level out of range), or a string that is not a valid
  `vMAJOR.MINOR.PATCH` tag at all. A malformed trust attempt is rejected loudly rather than silently
  ignored.

## How a harness consumes each group

- **`matrix`** — feed `inputs.authorship` and `inputs.review` to the level-assignment function; assert the
  result equals `expected.level`.
- **`classify`** — feed the raw `inputs` (signer identity class, trailers, policy, review facts) to the
  classifier; assert the derived authorship and review classes equal `expected.authorship` /
  `expected.review`, and the assigned level equals `expected.level`.
- **`precedence`** — parse every string in `ordered`, sort by the implementation's SemVer precedence, and
  assert the sorted sequence equals `ordered`. Equivalently, assert each entry has strictly lower precedence
  than the next; equal precedence is a failure.
- **`grammar`** — parse `tag`; assert `expected.outcome`, and for `trust_version` / `plain_version` assert
  the extracted `component_path`, `core`, `level`, `iteration`, and `prerelease` match.

## Versioning and stability

- Vector `id`s are stable. A published `id` is never renamed, reused, or given a different meaning.
- **Adding** vectors (new `id`s) is non-breaking and does not require a `spec_version` bump.
- **Changing** a vector's asserted values (`expected`, `ordered`, or `tag`) is a semantic change that MUST
  accompany a spec change and a `spec_version` bump — implementations pin to a `spec_version`, so silently
  altering an expectation would break conformance claims.
- `description` and `note` fields are editorial and may be refined without a version bump.

## License

The vectors and the validator in this directory are licensed under [Apache 2.0](LICENSE) so implementations
may vendor them freely. The specification prose remains CC BY 4.0 — see the repository root for the full
path→license map.

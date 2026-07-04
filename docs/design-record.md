<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# SemVer-Trust — Supporting Discussion & Design Record

**Companion to:** the SemVer-Trust specification (normative) — canonical location `semver-trust.md` in `github.com/semver-trust/spec`; drafted in this workspace as `semver-trust-spec-v0.1.md`
**This document:** explanatory — rationale, rejected alternatives, review findings, open threads, agent handoff
**Date:** 2026-07-04 · **Revision:** r5 (see revision history)
**Audience:** Both human engineering teams, and future AI agents continuing this work

---

## 1. Executive summary

This project retires `go-semver` (a Go utility for managing git tags with semantic versioning) and relaunches the concept for AI-driven development. The core idea: **when agents author a growing share of production code, a version number's implicit claim — "safe drop-in replacement" — needs explicit, verifiable evidence behind it.** SemVer-Trust (working name) defines trust levels T0–T3 derived from cryptographically verified provenance, aggregates them per release using weakest-link flooring with transitive propagation through the workspace dependency graph, encodes the result in SemVer pre-release identifiers so that low-trust releases are *opt-in by construction*, and publishes signed in-toto attestations as the portable, living record.

Two sentences carry the entire design; everything else is derivation:

1. **A version bump is a compatibility claim; a trust level is the strength of evidence behind the claim.**
2. **Trust levels measure attested accountability, not keystrokes.**

Current state: spec draft v0.1 complete and internally verified, committed to `github.com/semver-trust/spec` as `semver-trust.md`. Naming and repository topology are decided (ADR-013: the scheme is **SemVer-Trust**), and the licensing/control strategy is decided (ADR-014: Apache 2.0 for code and vectors, CC BY 4.0 for prose, with control carried by trademark + conformance gating, governance, and copyright). No implementation exists yet.

## 2. Project origin and intent

- **Starting point (Brad):** retire the `go-semver` repository; relaunch "for the AI age."
- **Founding concept (Brad):** use semantic versioning syntax to identify *trust levels* for a release — a release written and reviewed entirely by AI should not be trusted identically to one written and tested by humans. Included the instinct that a large-blast-radius change written solely by AI might warrant a "breaking" increment even when the same change, human-reviewed, would not.
- **Hard requirements issued during design (Brad):**
  1. Must work for non-OpenAPI-based projects.
  2. Must work for non-Golang projects.
  3. Path-scoped trust is required, because monorepos remain common in a post-AI world (agents favor them: context locality, atomic cross-cutting changes, single enforcement point).
- **Positioning:** the scheme sits beside SLSA/sigstore supply-chain work — human-legible, embedded in the version identifier, focused on *first-party* code provenance — rather than competing with them. The spec is deliberately separable from any implementation (the way SemVer-the-spec is separate from tools), so the idea can outlive one repo.
- **Strategic context (org-internal):** path-scoped trust produces a trust heatmap of the codebase over time — which zones are agent-run vs human-tended and how that boundary moves. This is effectively a per-scope **Presence** measurement (TAC KPI framework) with cryptographic backing instead of survey data: it converts "how much do we trust AI-written code" from a philosophy debate into a dashboard. Expect this to matter for leadership storytelling independent of the tool's engineering value.
- **Naming:** explored `trustver`, `vouch`, `attest`, `semver-agent`, `credence`, `lineage`, and others; leading candidates were `vouch` (evocative, works in a sentence) and `trustver` (discoverable). Decision was deferred at drafting time; **resolved by ADR-013** — the working name became the name, carried by the `github.com/semver-trust` organization. The spec's §12.6 placeholder caveat and the `<spec-domain>` predicate-URI placeholder remain, to be cleaned up in a spec v0.2 pass (§8).

## 3. Foundational principles and their derivations

These were *derived during discussion*, not assumed. Recording the derivations so future agents understand what breaks if a principle is relaxed.

**P1 — Bump = claim; trust = evidence.** Reframes the founding "AI blast radius = breaking change" instinct without discarding it: an unreviewed AI rewrite of core paths can't *evidence* a PATCH claim ("drop-in safe"), so either the claim escalates or the release waits in an opt-in channel for evidence. Avoids the trap of encoding *who* wrote code as inherently good/bad; encodes what has been *shown*.

**P2 — Accountability, not keystrokes.** Forced by the identity-laundering limit: a developer running an agent locally commits under their own key, and no cryptography distinguishes that from hand-typed code. Rather than pretend, the scheme defines a human signature as an accountability assertion ("this is mine, or I reviewed what was produced under my name"). Consequence: T2/T3 mean "human stands behind it." Hiding this limit would invite exactly the gaming that discredits the scheme; stating it normatively (spec §4.2) is a feature.

**P3 — Weakest link, objectively scoped.** Floors, never averages: one unreviewed autonomous commit can compromise everything around it. Scoping keys off git diff paths (objective ground truth), never declared intent (gameable). Direct corollary: **no de-minimis exception** — any "trivial commits don't count" rule becomes the hiding place for a payload.

**P4 — Degrade honestly.** Ecosystems without a compatibility differ can *prove* less, so more of their releases stay in the pre-release channel until humans or soak time supply what tooling couldn't. Less verification capability ⇒ lower provable trust, never equal trust with less backing. This also creates the right incentive gradient toward spec-first architecture (see ADR-004).

**P5 — Git tag canonical; attestation portable.** Two independent forcing functions: (a) PEP 440 cannot carry arbitrary pre-release identifiers, so any consumer parsing trust out of version strings is non-portable; (b) trust *evolves* after a version string is frozen (post-hoc review, revocation), so the living record must live in supersedable attestations while the tag records trust at release time.

**P6 — Levels order accountability, not risk (ADR-019; steelman review).** Trust levels claim *who stands behind* a change, never a predicted defect rate. Forced by the capability-parity boundary: as agent review quality approaches the human median, a high-evidence T1 release may empirically outperform a rubber-stamped T3 — read as risk-ordering the levels would be falsified by parity; read as accountability-ordering they remain true indefinitely. Risk mapping belongs to the policy layer via the evidence vector. P6 also buffers the keystone empirical claim (trust↔outcome correlation): accountability retains market value — someone to answer, liability attachment, incentive alignment — even if that correlation proves weak.

## 4. Decision record

Decisions live as **one file per ADR under `docs/adr/`** (maintainer convention),
indexed with statuses at `docs/adr/README.md`. Identifiers (ADR-001…) are stable
regardless of location; every ADR reference in this document resolves there.
Field format: Status / Date / Decision / Rationale / Rejected / Revisit trigger
(+ Supersedes where applicable). Unless a file states otherwise, status is
Accepted (draft v0.1).

| ADR | Title |
|---|---|
| ADR-001 | Encode trust in SemVer pre-release identifiers, not build metadata |
| ADR-002 | Trust levels count independent accountable humans |
| ADR-003 | Scalar level in the tag; full provenance vector in the attestation |
| ADR-004 | Derivation proofs are the only exception to weakest-link flooring |
| ADR-005 | Bump policy: semantic floor + evidence ceiling, two strategies |
| ADR-006 | Path-scoped trust with transitive propagation is first-class |
| ADR-007 | Configuration is the root of trust; meta-path violations hard-fail |
| ADR-008 | Unverifiable ≠ T0: verification failures abort |
| ADR-009 | Promotion: same SHA, new attestation; cascades; supersession over mutation |
| ADR-010 | Trust channel generalizes (and should not mix with) rc |
| ADR-011 | Language-agnostic core; ecosystem plugins; lossy registry projections |
| ADR-012 | External dependencies out of scope for v0.1 |
| ADR-013 | Naming and repository topology |
| ADR-014 | Licensing and control strategy |
| ADR-015 | Derivation inputs pin via language-native mechanisms, not environment managers |
| ADR-016 | Development environments: outcome-based convention, devbox as maintainer default |
| ADR-017 | Roadmap reorders around demand-side artifacts and keystone instrumentation |
| ADR-018 | Verification interfaces accept injectable trust roots and clock from day one |
| ADR-019 | Trust levels order accountability, not risk |

## 5. Design review findings (QA record)

The spec was reviewed *before and after* drafting; recording findings so future agents know these were considered, not missed.

**Caught before drafting (design-level):**

1. **Taxonomy hole** — human-authored/unreviewed code had no level → rederived levels around accountable-human count (ADR-002).
2. **Pre-release precedence interactions** — `rc` vs `t` ordering and the `t10 < t2` lexical hazard → single-digit levels, rc-generalization position (ADR-010).
3. **Immutable registries vs promotion** — version strings baked into npm/PyPI artifacts → republication-from-identical-SHA clause (ADR-009).
4. **Scalar/vector tension** → split responsibilities (ADR-003).
5. **Merge-commit conflict resolutions** are authored changes; PR review attestations don't automatically cover novel resolution hunks (spec §4.3.4).
6. **Dependency cycles** → SCC collapse (spec §5.3).
7. **Cascade re-evaluation** on dependency promotion via pinned floor sources (spec §7.3.4).

**Caught after drafting (document-level):**

8. **Worked-example arithmetic bug** — Appendix A step 4 originally claimed `effective(auth) = T3` after promoting `common`; correct is `min(own T3, common T2) = T2` (same clean-channel outcome, wrong level). Fixed.

**Mechanical verification performed on the spec document:**

- All `§` cross-references resolve to real sections/items.
- SemVer precedence claims (`rc.1 < t1.1`, `t1.1 <` clean, `t10 < t2`, `t0 < t2`) verified by implementing the SemVer comparison rules and testing.
- §3.2 level table ≡ Appendix B grid, and both satisfy the accountability invariant: `level = f(count of accountable humans, agent corroboration)`.
- The TOML policy example parses (`tomllib`); the JSON attestation example parses.

**Adversarial (steelman) review (2026-07-04):** full analysis at `docs/analysis/2026-07-04-steelman.md`. Keystone identified: E2 (trust↔outcome correlation), buffered by V1 (accountability's independent value) — collapse requires the conjunction, which held under pressure. Strongest internal counterargument found: the security-patch velocity conflict under `demote` (queued as a spec §12 open question rather than quietly patched). Dispositions: roadmap reorder (ADR-017), injectable trust roots/clock (ADR-018), P6 (ADR-019), spec v0.2 queue expansion. Standing predictions recorded in the analysis §5: Goodhart equilibrium → "accountability infrastructure first" framing; mixed-authorship decay of the authorship axis toward reviewer-counting; null-E2 repositioning path.

## 6. External facts relied upon (re-verify before implementation)

The design leans on ecosystem behaviors that were asserted from knowledge, not re-checked against live documentation during this session. They are stable and high-confidence, but any agent beginning implementation MUST re-verify against current docs — several are load-bearing:

| # | Fact relied upon | Load-bearing for |
|---|---|---|
| 1 | Go modules reject build-metadata suffixes; only `+incompatible` exists; nested-module tags use `dir/vX.Y.Z` | ADR-001, ADR-006 |
| 2 | Go modules / npm / Cargo exclude pre-release versions from default range resolution | ADR-001 (opt-in-by-construction) |
| 3 | PEP 440 pre-release segments limited to `a`/`b`/`rc` | ADR-011, P5 |
| 4 | SemVer 2.0.0 precedence: numeric identifiers < alphanumeric; alphanumerics compare ASCII-lexically; pre-release < release | ADR-010 (verified mechanically against spec rules, §5 above) |
| 5 | `golang.org/x/exp/apidiff`, `cargo-semver-checks`, `japicmp`, API Extractor exist and detect public-surface breakage | ADR-005, ADR-011 |
| 6 | sigstore gitsign (keyless commit signing), keyless workload identities via OIDC, Rekor transparency log | spec §4.2, §8.2 |
| 7 | in-toto Statement v1 (`https://in-toto.io/Statement/v1`) as the attestation envelope | spec §8 |
| 8 | Claude Code emits `Co-authored-by` trailers for agent-assisted commits | spec §4.1 |
| 9 | npm dist-tags can reference any published version, including pre-releases | ADR-011 |
| 10 | GitHub's new-repo license picker includes only CC0 among CC licenses; CC BY 4.0 must be added manually (**verified against the live UI, July 2026** — corrected an incorrect assertion made during discussion) | ADR-014 execution |
| 11 | GitHub license detection (Licensee) recognizes verbatim CC BY 4.0 text and badges it; dual-license repos surface a single badge or "View license" | ADR-014 execution |
| 12 | sigstore keyless signing certificates are short-lived by design; verification of historical signatures depends on transparency-log inclusion proofs | ADR-018, conformance fixture design |

## 7. Current state and artifacts

| Artifact | Status |
|---|---|
| GitHub organization `semver-trust` | **Exists** (created July 2026). Pending: `.github` profile repo/README as the org front door. |
| `spec` repository | **Exists**; contains the normative spec as `semver-trust.md` (content = draft v0.1). Design record, schemas, conformance vectors, `TRADEMARK.md`, and the dual-license arrangement not yet committed. |
| Normative spec | **Draft v0.2 produced 2026-07-04** (pending commit): resolves §12.6 and `<spec-domain>`, adds P6 + §3.1 clarification, mirrors ADR-015 into §4.4, adds §12.7–12.8; full delta in spec Appendix C; mechanical verification re-run clean. v0.1 baseline per §5: 12 sections + 2 appendices (trust model, provenance capture, aggregation/propagation, release evaluation + decision table, tag grammar, registry projections, attestation predicate sketch, TOML policy reference, verification algorithm, threat model, open questions, worked example, level grid). Placeholders remaining for the v0.2 pass: §12.6 naming caveat, `<spec-domain>` predicate URI. |
| This document | Explanatory companion, revision r2. |
| `TRADEMARK.md` | **Drafted** (ecosystem naming permitted with unofficial-status disclaimer; self-verified conformance claims; fork-rename rule; attribution≠affiliation clause; common-law status stated plainly). Pending commit; deserves IP-counsel review if traction arrives. |
| `semver-trust-go` repository | Planned per ADR-013; creation not yet confirmed. Implementation **not started**. |
| Formal JSON Schemas for predicates | Not started (spec §8.1 predicate is an illustrative sketch). |
| Review-attestation predicate (`…/review/v1`) | Named in spec §4.3; schema not drafted. |
| Conformance suite | Not started; elevated to *sync contract* between repos (ADR-013). |
| Predicate-type domain | **Registered: `semver-trust.dev`** (2026-07-04). Predicate URIs bound in spec v0.2 (§4.3 review, §8.1 release, both at `/…/v0.1`). Pending: GitHub Pages on the `spec` repo so predicate URLs resolve. |
| Name | **Decided:** SemVer-Trust (ADR-013). |
| Licensing & control | **Decided** (ADR-014); file arrangement pending per its implementation notes. CLA-vs-DCO deferred until the first external contribution. |
| Old `go-semver` repo | To be retired; migration/deprecation story not designed. |

## 8. Open threads and next steps

**Pressure-test with the team first** (predicted adoption-friction points, in order):

1. **Unverifiable → fail** (ADR-008, spec §5.2/§10): correct security posture, brutal on repos with pre-scheme history. Likely needs an *adoption boundary* concept — a designated first-verified tag before which history is exempt. Not yet designed.
2. **No de-minimis** (P3, spec §5.1): expect "why did a typo fix demote our release" complaints; the answer is derivation rules (add a formatter/docs derivation) — but docs-only changes have no derivation story yet. Possible gap: a `docs`-scope carve-out via scope weights vs. flooring. Undecided.
3. **Meta-path hard-fail** (ADR-007): interacts badly with agents that helpfully "fix" CI workflows mid-task. Contributor policy and agent contracts (CLAUDE.md) must warn agents off meta-paths explicitly.

**Then, roughly in order:**

4. ~~Decide the name; register the predicate-type domain~~ (done — ADR-013; `semver-trust.dev` registered 2026-07-04). Remaining: GitHub Pages on the `spec` repo with the custom domain so predicate URLs resolve to their definitions.
5. Populate the `spec` repo: layout (`spec/` or root spec file, `schemas/`, `conformance/`, `docs/`), dual-license arrangement per ADR-014 implementation notes, commit `TRADEMARK.md` and this design record, create the org `.github` profile repo.
6. ~~Spec v0.2 pass~~ (executed 2026-07-04; delta in spec Appendix C; steelman Appendix A discharged). Remaining from the batch: formalize the JSON Schemas for the release and review predicates (`schemas/`, Apache 2.0), now against the bound URIs.
7. Build the **conformance suite** (level-assignment matrix as data, precedence vectors, fixture repositories with expected verification outcomes and attestations). Precedes serious implementation work because it *is* the implementation's acceptance test and the cross-repo sync contract (ADR-013).
8. Reference implementation in `semver-trust-go` (richest evidence-provider story: `apidiff`, coverage, `go list` graph adapter): CLI surface sketched as `verify` (walk range, report per-commit provenance), `release` (evaluate + tag + attest), `policy` (validate config); plugin interfaces for evidence providers, graph adapters, registry projections. It MUST release *itself* with trust-tagged releases as the flagship demo — which promotes the *adoption boundary* gap (pressure-test #1) from open thread to first implementation requirement. Verification interfaces accept injectable trust roots and an injectable clock from day one (ADR-018). At equal priority, per ADR-017: a minimal demand-side consumer (a `verify` GitHub Action + README trust badge) and retrospective trust profiling of existing repositories — the E5 fix and the E2 test, respectively.
9. Dogfood target #2: Brad's Go API starter repo (oapi-codegen) — it already has the human-reviewed-contract philosophy and a `CLAUDE.md` agent contract; its OpenAPI derivation rule is the flagship ADR-004 demonstration.
10. Design the `go-semver` retirement/redirect story (deprecation notice pointing at the org).
11. Revisit spec §12 open questions as evidence accumulates (T1 efficacy, trust decay, SLSA mapping, cross-repo propagation). Note the irony recorded for honesty: the project defining transitive trust for monorepos chose a polyrepo for itself, so cross-repo trust (spec §12.4) will eventually be felt firsthand.

## 9. Agent handoff contract

Instructions to any agent (or human) resuming this work:

1. **Document precedence:** the spec — `semver-trust.md` in `github.com/semver-trust/spec` — is normative. This document explains *why*; where they conflict, the spec wins and the conflict should be reported as a defect.
2. **Do not re-litigate rejected alternatives** (ADR "Rejected" entries) without *new evidence or a changed requirement*. In particular: build-metadata encoding (ADR-001), de-minimis exemptions (P3/ADR-004), unverifiable→T0 (ADR-008), and inflation-as-only-strategy (ADR-005) were each rejected for stated reasons that have not changed.
3. **Change protocol:** decisions change by *superseding* — create `docs/adr/NNNN-slug.md` with the next number and a `Supersedes:` field; never edit an accepted ADR's Decision/Rationale/Rejected content in place (the sole permitted edit to a superseded file is its Status line, set to `Superseded by ADR-NNN`). Update the `docs/adr/README.md` index. Mirror material changes into the spec with a version bump of the spec itself.
4. **Before implementing anything**, re-verify §6 facts against current ecosystem documentation; several postdate nothing but all predate you.
5. **Terminology discipline:** use the spec's §2 terms exactly (own trust vs effective trust; scope vs component; channel; accountable human). Drift here has already been the source of one caught bug (§5.8).
6. **Honesty clauses are load-bearing:** P2 (accountability, not keystrokes) and P4 (degrade honestly) are commitments, not caveats. Any feature that quietly claims more than the evidence supports — e.g., inferring authorship the signatures can't prove, or waiving evidence where a differ is missing — violates the design's core defense against being discredited.
7. **Where to start coding:** spec §10 (verification algorithm) is the implementation skeleton; ADR-011 defines the plugin seams; §8 item 8 above sketches the CLI. Start with `verify` against a synthetic fixture repo before touching `release`.
8. **Context that won't be in the repo:** the founding conversation reframed "AI blast radius should force a breaking change" into the semantic-floor/evidence-ceiling split (ADR-005) — if a stakeholder asks why big AI changes don't bump MAJOR, that reframing (P1) is the answer, and `strategy = "inflate"` exists for orgs that insist.
9. **Agent-contract files:** `AGENTS.md` is the canonical per-repo agent contract — vendor-neutral, matching the project's own thesis — and `CLAUDE.md` is a two-line pointer for tools that read only that file. Replicate the pair in every repository.

---

## Appendix: Conversation timeline (condensed)

1. **Naming exploration** for a `go-semver` successor "for the AI age" → surfaced trust/provenance-centric candidates; deferred.
2. **Founding concept** (Brad): semver-encoded trust levels; AI-authored large-blast-radius changes as possibly "breaking."
3. **Design session:** four enforcement points (commit / merge / release / consume + attestation store); trust taxonomy v1; weakest-link flooring; reproducibility exception for generated code; pre-release-identifier encoding discovered as the key trick (opt-in by construction; Go build-metadata blocker); bump-claim reframing (P1); identity-laundering limit → accountability principle (P2).
4. **Generalization requirements** (Brad): non-OpenAPI, non-Go, path-scoped monorepo trust → derivation proofs (ADR-004), plugin architecture (ADR-011), transitive propagation with the auth/billing/common worked example (ADR-006), meta-paths (ADR-007).
5. **Spec drafting with review** ("double-check your work"): four design-level fixes pre-draft, mechanical verification post-draft, one arithmetic bug caught and fixed (§5).
6. **This document** (r1).
7. **Repository topology** (Brad: two repos, spec + Go implementation) → conformance-suite-as-sync-contract insight; org recommendation → `github.com/semver-trust` created; naming resolved as a conscious side effect of repo creation → ADR-013.
8. **Licensing** (Brad: control vs. traction weighing) → ADR-014, control moved to trademark/governance/copyright levers; execution correction — GitHub's picker offers no CC BY (verified live; CC0 rejected as inverted intent) → manual verbatim paste; `TRADEMARK.md` drafted as ADR-014 lever (a).
9. **Spec committed** to the `spec` repo as `semver-trust.md`; design record revised to r2. Root files landed: `LICENSE` (CC BY 4.0 legalcode, verbatim incl. the CC trailer block), `LICENSE-APACHE` (nit fixed: hyphen), `TRADEMARK.md`, README license map, `CONTRIBUTING.md` CLA/DCO guard, `CLAUDE.md` agent contract.
10. **ADR extraction**: 14 ADRs relocated verbatim to one-file-per-decision layout with index; design record §4 became the pointer/index; r3.
11. **`semver-trust-go` starter set:** provenance hygiene from commit #1 (signing, trailers, merge-commits-only) as a project deliverable; contract convention corrected after a tool-agnosticism review (Brad) to **AGENTS.md canonical + CLAUDE.md pointer**; `.gitmessage` trailer examples neutralized across agent tooling.
12. **Environment tooling evaluation** (devbox/direnv vs. 2026 alternatives; mise Go-issue follow-ups dissolved on inspection) → ADR-015 (self-contained derivation pins — extends P5 to verification portability) and ADR-016 (outcome-based convention, devbox maintainer default, explicit mise trigger).
13. **Steelman analysis** (maintainer-directed) of specification and codification strategy → `docs/analysis/2026-07-04-steelman.md`; ADR-017 (demand-side artifacts + keystone instrumentation), ADR-018 (injectable trust roots/clock), ADR-019 (P6); spec v0.2 queue expanded; r4.
14. **Domain registered** (`semver-trust.dev`, 2026-07-03) → **spec v0.2 pass executed** per §8.6: placeholders resolved, P6 and ADR-015 mirrored, §12.7–12.8 added, predicate URIs bound (review predicate aligned `v1`→`v0.1` pre-first-attestation); verification suite re-run clean; this revision (**r5**).

---

## Revision history

| Rev | Date | Changes |
|---|---|---|
| r1 | 2026-07-04 | Initial record: principles P1–P5, ADR-001…012, QA record, external-facts table, handoff contract, timeline 1–6. |
| r2 | 2026-07-04 | Added ADR-013 (naming/topology) and ADR-014 (licensing/control); §1 and §2 updated for resolved naming; §6 facts 10–11 added; §7 current-state table rebuilt around live repos; §8 next steps renumbered (4–11) with domain registration on the critical path; §9 cross-references updated (items 1, 7); timeline 7–9; this table. |
| r3 | 2026-07-04 | ADRs extracted verbatim to `docs/adr/` (one file each + index); §4 converted to pointer + title index; §9 change protocol updated with file-per-ADR mechanics; document destined for `docs/design-record.md`; timeline 9 amended for root-file completion, entry 10 added. |
| r4 | 2026-07-04 | Steelman review integrated: P6 added to §3; §5 adversarial-review block; §6 fact 12; §4 index rows ADR-015…019; §8 items 6 and 8 expanded (v0.2 queue with Appendix-A pointers; ADR-017/018 requirements); §9 item 9 (AGENTS.md convention); timeline 11–13. |
| r5 | 2026-07-04 | Domain registration recorded; spec v0.2 pass marked executed (§7 rows, §8 items 4 and 6); timeline 14. |

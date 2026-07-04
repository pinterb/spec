<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-019 — Trust levels order accountability, not risk

**Status:** Accepted (2026-07-04)
**Date:** 2026-07-04
**Decision:** adopt principle **P6**: T-levels order attested human accountability; they are not an empirical risk ordering. Risk mapping is the policy layer's job, consuming the full evidence vector (differ proofs, coverage, blast radius) through configurable decision tables. To be mirrored into the spec at v0.2 — a §1.1 principle entry, a §3.1 clarification sentence, and a §12 open question on empirical validation — with ready-to-paste text in docs/analysis/2026-07-04-steelman.md Appendix A.
**Rationale:** the capability-parity boundary (steelman §3.2.2): as independent agent review approaches median human review quality, a high-evidence T1 release may empirically outperform a rubber-stamped T3. Read as a risk ordering, the levels would be falsified by parity; read as an accountability ordering, they remain true indefinitely. P6 also buffers the keystone (E2): even if the trust↔outcome correlation proves weak, accountability retains independent market value — someone to answer, liability attachment, incentive alignment — so the scheme's honest fallback is *accountability infrastructure first, quality signal second*, adopted deliberately rather than conceded to critics.
**Rejected:** renaming to "accountability levels" (churn; the T-notation is established; the clarification suffices); embedding risk weights into level definitions (conflates taxonomy with policy; Goodhart accelerant).
**Revisit trigger:** empirical E2 results (ADR-017) inform *policy defaults*, never the level semantics.

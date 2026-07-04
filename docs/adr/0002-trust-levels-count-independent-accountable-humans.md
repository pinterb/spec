<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-002 — Trust levels count independent accountable humans

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** T0 = zero accountable humans; T1 = zero humans + independent agent corroboration; T2 = exactly one accountable human (either role); T3 = two distinct accountable humans (author ≠ reviewer).
**Rationale:** the original taxonomy (T0 AI/none, T1 AI/AI, T2 AI/human, T3 human/human) was authorship-centric and **incomplete — human-authored/unreviewed code had no level** (caught in the pre-spec review pass). Rederiving from P2 produced a complete, principled scale: every authorship × review cell maps, and the ordering follows from counting independent accountability rather than from opinions about AI code quality.
**Consequence accepted deliberately:** `human+unreviewed` and `agent+human-reviewed` both map to T2 at the tag level. Policies needing the distinction consume the full provenance vector in the attestation (ADR-003).
**Rejected:** bolting extra levels onto the original four (ad hoc, ordering disputes); making human-unreviewed T1-adjacent (equates one accountable human with zero).
**Revisit trigger:** empirical evidence on T1 efficacy (spec §12.1) could justify re-pricing, not restructuring.

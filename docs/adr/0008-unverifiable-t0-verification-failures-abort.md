<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-008 — Unverifiable ≠ T0: verification failures abort

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** a commit whose signature or required attestations cannot be verified has *no* level; the release fails.
**Rationale:** T0 is a verified fact about a verified commit ("no accountable human"). Mapping verification *failure* to T0 would let an attacker degrade gracefully into the pre-release channel instead of being stopped, and would poison the meaning of T0 for analytics.
**Rejected:** unverifiable→T0 fallback.
**Revisit trigger:** adoption friction (flagged as a pressure-test item, §8).

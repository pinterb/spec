<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-012 — External dependencies out of scope for v0.1

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** effective trust covers first-party code; third-party dependencies remain the domain of SLSA/sigstore/SCA. Policy MAY impose separate external requirements; a SLSA-level ↔ T-level mapping is deliberately undefined.
**Rationale:** scope containment. Cross-boundary trust likely flows through consuming the dependency's *own* release attestation — deferred (spec §12.3–12.4).

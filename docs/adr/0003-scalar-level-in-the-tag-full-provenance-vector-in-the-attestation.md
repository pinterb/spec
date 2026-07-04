<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-003 — Scalar level in the tag; full provenance vector in the attestation

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** the tag carries only `t<level>`; the attestation preserves per-commit authorship class, review class, identities, and derivations.
**Rationale:** a 2-D (or richer) encoding in the version string is unreadable and unsortable; but collapsing to a scalar loses policy-relevant detail. Splitting responsibilities resolves the tension: scalar for encoding/precedence/humans, vector for machines/policy.
**Rejected:** matrix-style identifiers in the tag (`t-a2r1`-like schemes).

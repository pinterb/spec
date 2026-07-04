<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-009 — Promotion: same SHA, new attestation; cascades; supersession over mutation

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** promotion re-evaluates the identical commit SHA with new evidence and cuts the clean tag on it; immutable registries (npm/PyPI) get republication *from the identical source SHA* (the source binding, not artifact-digest equality, is the guarantee absent reproducible builds); dependency promotions cascade to downstream re-evaluation via pinned floor sources; demotion is expressed by superseding attestations, never by un-publishing.
**Rationale:** resolves the immutability tension (trust evolves; version strings don't) and the "auth stuck because common was T0" case without rebuilds. Registry metadata baking the version string in (caught in review) forced the republication clause.
**Rejected:** re-tagging as the universal mechanism (breaks on immutable registries); mutable trust markers on existing versions (nothing downstream could cache decisions).

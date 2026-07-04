<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-011 — Language-agnostic core; ecosystem plugins; lossy registry projections

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** everything touching git (capture, verification, aggregation, encoding, policy) is universal; compatibility differs (`apidiff`, `cargo-semver-checks`, `japicmp`, API Extractor), coverage, fan-in, and workspace graphs are plugins; registries receive projections (npm native + dist-tags; Cargo native; PyPI lossy → `rc<n>` + attestation-only trust).
**Rationale:** Requirement 2, combined with P4: where a plugin is missing, evidence requirements bind tighter rather than being waived. PyPI's PEP 440 limitation is the existence proof for P5.
**Rejected:** requiring differ support for adoption (would exclude most ecosystems); normalizing all registries to a lowest common denominator (Go/npm can carry more signal — let them).

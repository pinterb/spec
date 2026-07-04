<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-018 — Verification interfaces accept injectable trust roots and clock from day one

**Status:** Accepted (2026-07-04)
**Date:** 2026-07-04
**Decision:** in `semver-trust-go` (and recommended for all implementations), every verification path accepts explicitly injected trust material — allowed-signers registries, CA and transparency-log roots, identity maps — and an injected verification clock. No package-level globals, no implicit system time, no ambient network trust-root fetching in core verification. Conformance fixtures include vendored long-lived test keys alongside sigstore-keyless cases, and fixture expectations pin the clock and roots they verify under.
**Rationale:** fixture aging is where the conformance-suite-as-sync-contract argument is weakest (steelman §3.2.6): keyless signing certificates are short-lived by design and historical verification depends on transparency-log inclusion, so naive fixtures rot and the suite decays to testing only the timeless core (levels, precedence, aggregation) while skipping cryptographic verification — the hard part. Injection makes fixtures verifiable indefinitely under pinned roots and clock, and is the same capability retrospective profiling (ADR-017) requires, retrospection being inherently verification of the past.
**Rejected:** keyless-only fixtures (rot); regenerating fixtures per CI run (tests the generator, masks verifier regressions, breaks cross-implementation identity of the vectors); system-clock verification with tolerance windows (unreproducible, drifts).
**Revisit trigger:** none foreseen — this is an interface invariant.

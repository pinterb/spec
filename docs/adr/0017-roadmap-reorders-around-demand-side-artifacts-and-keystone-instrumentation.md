<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-017 — Roadmap reorders around demand-side artifacts and keystone instrumentation

**Status:** Accepted (2026-07-04)
**Date:** 2026-07-04
**Decision:** the roadmap is reordered: alongside — not after — the reference CLI core, build (a) a minimal demand-side consumer, a `verify` GitHub Action emitting a README trust badge ("SemVer-Trust: T2 ✓"), and (b) **retrospective trust profiling** — computing would-have-been trust profiles for existing repositories from historical signatures and platform review data. Attestation ergonomics (`.gitmessage`, `--trailer`, merge-attestation workflows) are treated as product surface, not hygiene, because T2 is the expected volume tier.
**Rationale:** steelman findings (docs/analysis/2026-07-04-steelman.md): E5 — consumer demand — is unverified but *fixable by us*; E2 — the trust↔outcome keystone — is *testable by us* via retrospection against CVE/incident history, and retrospective profiling doubles as a zero-commitment onboarding moment ("what's my repo's trust profile"). The steelman's own window-urgency argument makes visible-adoption ordering dominate thoroughness ordering, and badges are the precedented zero-friction adoption wedge (coverage badges, goreportcard).
**Rejected:** the prior thoroughness-ordered roadmap (optimizes completeness while the calibration window closes); building full policy-engine integrations (OPA/Kyverno) first (heavier lift, later demand); deferring E2 testing to post-1.0 (keystone risk compounds with sunk cost).
**Revisit trigger:** results of retrospective E2 studies in either direction — a null result activates the P6 repositioning (ADR-019; analysis §5.3).

<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-006 — Path-scoped trust with transitive propagation is first-class

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** policy maps path globs → named scopes; per-scope floors compute from commits *touching* the scope (diff paths); `effective(C) = min(own(C), min effective(deps))` over the workspace graph via pluggable graph adapters; dependency cycles collapse to their SCC's minimum.
**Rationale:** Requirement 3. Propagation is what makes scoping safe rather than cosmetic — without it, risk launders into shared libraries while consumers' scopes stay pristine (the pre-transitive-analysis failure mode of dependency scanners). Side effect with correct incentives: shared packages become the highest-ROI place to spend human review, since their level multiplies across consumers. Component tags (`auth/v1.4.0-t2.1`) align with Go nested-module conventions and existing monorepo release tooling.
**Rejected:** scalar repo-wide trust (original default — punishes monorepos); scope independence without propagation (laundering); commit-message or CODEOWNERS-declared scoping (subjective; diff paths are ground truth).

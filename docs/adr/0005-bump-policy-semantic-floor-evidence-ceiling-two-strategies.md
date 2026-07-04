<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-005 — Bump policy: semantic floor + evidence ceiling, two strategies

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** the semantic floor (compat differ ≻ conventional commits) sets the *minimum* bump — no trust level overrides an API break. The evidence ceiling (risk ∝ blast radius × inverse trust) constrains the *claim*; when unsupported, policy applies **`demote`** (recommended: correct bump, pre-release channel) or **`inflate`** (escalate the bump).
**Rationale:** Brad's founding instinct (AI + large blast radius ⇒ breaking) is *right about risk* but, implemented as pure bump inflation, conflates two signals: MAJOR tells consumers "your code must change," which is false when only confidence differs. Inflation dilutes the one signal SemVer defends, forces empty migration reviews, and burns major numbers. Demotion preserves API semantics while keeping risk out of default resolution. Both are supported because some orgs legitimately want risk in the precedence-relevant digits.
**Rejected:** inflation-only (above); trust-blind classic semver (ignores the founding problem); numeric blast-radius formula in the spec (false precision invites gaming — inputs are normative, scoring is implementation policy).

<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-010 — Trust channel generalizes (and should not mix with) rc

**Status:** Accepted (draft v0.1)
**Date:** 2026-07-04
**Decision:** projects adopting the scheme should not combine `rc`-style identifiers with trust identifiers on one version; a below-threshold release *is* the release candidate, with the trust level stating why it isn't clean.
**Rationale:** rc's traditional lifecycle — publish, soak, gather evidence, promote — is exactly the trust-promotion lane. Also pins two precedence facts verified mechanically: `rc.1 < t1.1 < (clean)` under ASCII comparison, and `t10 < t2` lexically — the latter forecloses multi-digit levels (levels are a fixed single digit).
**Rejected:** composing both (`-rc.1.t1`): precedence spaghetti with no added meaning.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-023 — Merge commits are created locally, signed and trailered, never by web-flow

**Status:** Accepted (2026-07-11)
**Date:** 2026-07-11
**Decision:** in the project's own repositories, pull requests are merged by the maintainer **locally** —
`git merge --no-ff` producing a merge commit that is signed by the maintainer's enrolled key and carries the
same `Provenance:` trailers every other commit carries — and the result is pushed to the protected branch.
Merging through the GitHub web UI (the `web-flow` committer) is not used. This resolves decision packet D1
from the implementation plan: web-UI merge commits are authored and signed by GitHub's `web-flow` identity
and carry no trailers, which classifies as *ambiguous* under §3.2 and floors to the agent-authored row —
poisoning the project's own trust level at dogfood time. Branch protection continues to require PRs and green
checks; only the merge *mechanics* move to the maintainer's machine. History already merged via web-flow
before this decision is left as-is and will surface honestly in retrospective profiling (P2: measure what the
signatures prove, nothing more).
**Rationale:** the repository's unbroken scheme-compliant history is a project deliverable in itself
(implementation-plan ground rules); a merge commit is a commit like any other under §3.2 and §4.3.4, so an
unsigned-by-a-person, untrailered merge is a standing hole in that deliverable. Of the two D1 options, local
merges need no spec change and no new identity class — they make merge commits satisfy the existing rules
instead of carving an exception for a hosting platform's convenience identity. The cost (the maintainer
merges from a terminal instead of a button) is the honest price of the scheme applying to itself.
**Rejected:** defining workflow-attested web merges as a recognized identity class (a real §4.2/v0.3
candidate for multi-maintainer projects, but a spec change with its own attestation machinery — deliberately
deferred until a project that cannot merge locally needs it, and revisitable then); treating web-flow merges
as exempt plumbing (there is no de-minimis exception, P3 — a merge commit with a conflict resolution is
authored code, §4.3.4); squash merges to avoid merge commits entirely (forbidden, §4.3.3: they rewrite
authorship and destroy per-commit provenance).
**Revisit trigger:** a second maintainer or a project constraint that makes local merging impractical; or
platform support for signed, trailered merges under the merging user's own identity — either reopens the
workflow-attested-merge option as a v0.3 spec question (§12).

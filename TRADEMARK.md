# SemVer-Trust Trademark Policy

"SemVer-Trust" is the name of this specification and project (the "mark").
This policy explains how the name may be used. Its goals are simple:

- **Anyone** may read, implement, teach, criticize, and build on SemVer-Trust.
- **No one** may create confusion about what SemVer-Trust is, which
  specification is authoritative, or which implementations conform to it.

The licenses on this repository (CC BY 4.0 for specification text, Apache 2.0
for schemas and conformance vectors) grant rights to the *content*. They do
not grant rights to the *name*. Attribution required by CC BY 4.0 does not
imply affiliation with or endorsement by this project.

## Uses that never require permission

- Truthfully referring to SemVer-Trust in articles, talks, documentation,
  academic work, comparisons, and criticism.
- Stating that your software **implements** SemVer-Trust, identified by
  specification version (e.g., "implements SemVer-Trust v0.1"), where the
  statement is accurate.
- Making a **conformance claim** under the conditions below.
- Naming an implementation package or repository in the ecosystem style
  `semver-trust-<qualifier>` (e.g., `semver-trust-rs`, `semver-trust-maven`),
  provided that (a) the project prominently states it is unofficial and not
  maintained by the SemVer-Trust project, and (b) it makes no conformance
  claim unless it meets the conditions below. Implementations may be adopted
  into the official organization by agreement, at which point the disclaimer
  is dropped.

## Conformance claims

The claim "**SemVer-Trust conformant**" (or equivalent wording) may be made
only when all of the following hold:

1. The implementation passes the complete conformance suite published in
   this repository (`conformance/`) for a released specification version.
2. The claim states that version explicitly: "SemVer-Trust v0.1 conformant."
3. The claim is withdrawn or re-verified when the implementation changes or
   when claiming conformance to a newer specification version.

Conformance is verified by the suite, not granted by this project — if your
implementation passes, you may say so. Publishing your conformance test
output alongside the claim is encouraged; verifiable claims are the point of
this project.

## Derivative specifications

The specification text may be forked, modified, translated, and republished
under its license. However, a **modified** specification must be published
under a different name and must not be presented as SemVer-Trust, a version
of SemVer-Trust, or a successor to it. Unmodified copies and translations
may retain the name and must identify the version copied and link to the
canonical repository. Translations should state that the English text is
authoritative.

## Uses that require permission

- Using the mark, or a confusingly similar name, in the name of a company,
  product, service, domain, or specification.
- Implying sponsorship, endorsement, or official status of anything not
  published by this project.

To request permission, open an issue in this repository.

## Status and changes

The mark is currently claimed at common law and is not registered. This
policy may be revised; the version in the default branch of this repository
is current. Good-faith uses that were permitted when made will not be
treated as violations retroactively.

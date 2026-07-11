<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# ADR-022 — Attestation signatures are SSHSIG over the DSSE PAE with purpose-binding namespaces

**Status:** Accepted (2026-07-11)
**Date:** 2026-07-11
**Decision:** for the SSH key family, a SemVer-Trust attestation signature is an OpenSSH SSHSIG
(PROTOCOL.sshsig) computed **over the DSSE pre-authentication encoding** of the envelope —
`PAE(payloadType, payload)` = `"DSSEv1" || SP || LEN(payloadType) || SP || payloadType || SP ||
LEN(payload) || SP || payload`, with lengths as ASCII decimal and payload the exact serialized statement
bytes — in the signature namespace **`attestation@semver-trust.dev`**. In the DSSE envelope, `sig` carries
the base64 of the armored SSHSIG and `keyid` carries the signer's SHA256 fingerprint. `keyid` is an
**untrusted lookup hint only** — verification resolves the public key embedded in the SSHSIG against the
injected attestation-signer registry (ADR-018); no keyid value is ever a trust anchor. Attestation signers
are enrolled in a **registry separate from the commit-signing registry**, scoped to the attestation
namespace: authorization to sign commits does not imply authorization to issue release or review
attestations, and vice versa.
**Rationale:** DSSE's PAE preserves the envelope's payload binding, so signing the PAE keeps standard DSSE
semantics; carrying the signature as an SSHSIG adds what raw signatures lack — a namespace that
cryptographically binds the signature's *purpose*. A git commit signature (`namespaces="git"`) can never be
replayed as an attestation signature and an attestation signature can never vouch for a commit, closing a
cross-protocol reuse channel that raw Ed25519-over-PAE leaves open. The convention also keeps the whole SSH
key family on one toolchain: `ssh-keygen -Y sign`/`-Y verify` produce and check these signatures directly
against `allowed_signers` files, which is what makes the conformance fixtures deterministic, independently
cross-verifiable, and reproducible without bespoke tooling (fixture plan §6). The registry split is
least-privilege at the trust-root level, expressed in the same allowed-signers format the rest of the
scheme already injects.
**Rejected:** raw Ed25519 over the PAE (standard-adjacent but purpose-blind: the same key's commit and
attestation signatures become interchangeable bytes, and generation/verification falls outside the OpenSSH
toolchain); reusing the `git` namespace for attestations (preserves the toolchain but reopens the reuse
channel the namespace exists to close); treating `keyid` as the trust anchor (§8.2: the signature inside
the attestation is the anchor and storage/hints are never trusted — resolving trust through a hint would
invert that); a single shared registry with both purposes enrolled per key (loses the least-privilege
boundary between "may commit" and "may attest").
**Revisit trigger:** GO-032 / D4 — sigstore keyless workload identities produce DSSE bundles under
sigstore's own conventions, which will coexist with this SSH-family profile and may warrant folding both
into one attestation-verification profile; or a second implementation whose platform cannot invoke OpenSSH
tooling, which would argue for adding the raw-signature form as a parallel profile.

# CRM5-DPRIME-IR-SAFE-EXACT-COMPOSITION-SOURCE-SEARCH-V2

**Date:** 2026-08-26
**Scope:** One new primary-source family outside the local quadratic-gravity,
Bjorken, 2D Yang--Mills, FQHE, massive O(N), and quantum-graph corpus
**Result:**
`EXACT_MARKED_PROJECTIVE_AMPLITUDE_IDENTITY__PHYSICAL_C_AND_RUNNING_COUPLING_NOT_SOURCE_DEFINED`

## Frozen candidate

The V2 search tested the exact massless factorized-scattering description of
the unitary renormalization-group flow from tricritical Ising to critical
Ising. Fendley, Saleur, and Zamolodchikov define the minimal models perturbed
by `Phi_13`, give the mass scale `M proportional to
|delta_beta|^((t+1)/4)`, and construct exact massless kink S matrices
([arXiv](https://arxiv.org/abs/hep-th/9304051),
[DOI](https://doi.org/10.1142/S0217751X93002277)). Their thermodynamic Bethe
ansatz produces a nonperturbative c-function across the RG crossover.

For the `t=4` tricritical-Ising-to-Ising flow, the RSOS labels collapse to one
left mover and one right mover, and the source gives

`S_RL(theta) = -tanh(theta/2 - i*pi/4)`.

The source kinematics are `p_R=(M/2) exp(theta_R)` and
`p_L=-(M/2) exp(-theta_L)`. Therefore the Lorentz invariant for a mixed pair
is, without fitting,

`s = M^2 exp(theta_R-theta_L)`,

so the additive rapidity difference is

`theta = log(s/M^2)`.

The exact amplitude has unit modulus for real `theta` and two finite,
distinguishable limits:

- `theta -> -infinity`: `S_RL -> +1`;
- `theta -> +infinity`: `S_RL -> -1`.

This is a finite on-shell amplitude in a massless integrable 1+1D model. It is
not presented as a four-dimensional inclusive IR-safe observable, and the
non-gauge scalar theory supplies no general gauge-invariance transfer.

## Exact marked projective identity

Writing `z=exp(theta)`, the source formula is equivalently

`S_RL = (1+i z)/(1-i z)`.

Orient the endpoints as `b_minus=+1`, `b_plus=-1`, and audit-mark the midpoint
response `e=S_RL(0)=i`. The normalized cross-ratio is then

`R(S) = i (1-S)/(1+S)`.

Direct substitution gives the exact, coefficient-free identity

`R(S_RL(theta)) = exp(theta) = s/M^2`.

Thus the amplitude supplies a mathematically exact marked projective
near-hit. Multiplying two such ratios induces a binary operation with

`C_induced(S_RL(theta_1),S_RL(theta_2)) = S_RL(theta_1 + theta_2)`

and audit identity `S_RL(0)=i`.

## Why the physical composition gate remains open

The last operation is induced by this audit; it is not the source's physical
composition statement. The source defines factorized scattering through the
Yang--Baxter consistency relation

`S12(theta12) S13(theta13) S23(theta23)
 = S23(theta23) S13(theta13) S12(theta12)`.

This multiplies pairwise scattering operators for a three-particle state at
their respective rapidity differences. It neither combines two scale
responses into `S_RL(theta_1 + theta_2)` nor marks the value `i` as a physical
identity response. Replacing the Yang--Baxter relation with the induced
cross-ratio law would therefore conflate multiparticle consistency with
response composition.

Two further transfer gates stay open:

1. the physical amplitude lies on the complex unit circle, not on Paper V's
   declared real response interval;
2. the source supplies a relevant coupling-to-mass relation and an exact TBA
   RG crossover, but it does not identify a running scalar coupling with this
   amplitude or with the audit-induced operation.

## Reproduction

```bash
python scripts/paper5/dprime_massless_rg_scattering_gate.py
python -m pytest tests/test_dprime_massless_rg_scattering_gate.py -q
```

Artifact:

`results/paper5/DPRIME_MASSLESS_RG_SCATTERING_GATE_2026-08-26.json`

## Verdict and claim boundary

This single-family search found one exact algebraic projective near-hit and
zero complete physical D' candidates. The exact identity is retained because
it sharply localizes the missing premise: a source-defined physical response
law, neutral identity, real-response transfer, and running-coupling
identification. No physical D' derivation, four-dimensional scattering
transfer, cosmology result, UV completion, RH result, or abc result follows.

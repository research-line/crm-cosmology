# CRM5-DPRIME-EXTERNAL-IR-SAFE-COMPOSITION-SEARCH-V1

**Date:** 2026-08-26
**Scope:** External search beyond the exhausted local quadratic-gravity corpus,
the Bjorken effective-charge chain, and the 2D Yang--Mills control
**Result:**
`EXACT_IR_FINITE_TRANSPORT_DPRIME_FAIL__SCALAR_C_NOT_SOURCE_DEFINED`

## Frozen search contract

A complete physical D' candidate had to supply, in one source-bound setting:

1. a physical gauge-independent or gauge-invariant IR-safe scattering or
   transport observable;
2. two finite, distinguishable, predeclared boundary responses;
3. an independently source-defined exact nonperturbative binary composition
   law for that observable;
4. coupling running or a source-defined RG crossover on a declared additive
   scale; and
5. a constant projective generator after the observable, boundaries, and
   scale were frozen.

No commensurate-scale relation, RG-flow transitivity, full scattering-matrix
composition, or fitted coordinate was allowed to stand in silently for the
missing scalar response law.

## Strongest near-candidate

Fendley, Ludwig, and Saleur compute the exact linear point-contact conductance
at filling fraction `nu=1/3` in the integrable boundary sine-Gordon
description of fractional-quantum-Hall edge transport
([arXiv](https://arxiv.org/abs/cond-mat/9408068),
[PRL](https://doi.org/10.1103/PhysRevLett.74.3005)). The calculation uses an
exact momentum-dependent `2 x 2` kink/antikink boundary S matrix and a
thermodynamic-Bethe-ansatz occupation problem. The physical conductance is a
weighted momentum integral involving `|S_++|^2`; it is not an S-matrix entry.

The source fixes the boundary scale

`T_B proportional to lambda^(1/(1-nu))`

and gives two finite conductance endpoints. With `G0=e^2/(3h)` and
`t=log(T/T_B)`, they are

- `t -> -infinity`: `G/G0 -> 0`, with `G/G0 ~ A exp(4t)`;
- `t -> +infinity`: `G/G0 -> 1`, with
  `1-G/G0 ~ B exp(-(4/3)t)`.

Thus this is a genuine physical, exactly computed, IR-finite transport
near-candidate with a declared boundary RG crossover. No separate gauge-fixing
parameter enters the conductance; the audit makes no broader gauge theorem
claim.

## Predeclared D' endpoint gate

Freeze the only affine normalization set by the two source endpoints,

`x = 2 G/G0 - 1`.

For a lower-boundary law `G/G0 ~ A exp(p_minus t)`, direct differentiation
gives

`(dx/dt)/(1-x^2) -> p_minus/2`.

For an upper deficit `1-G/G0 ~ B exp(-p_plus t)`, the same quotient tends to
`p_plus/2`. The coefficients `A` and `B` cancel, so no fit is involved. The
source exponents yield

- lower endpoint: `4/2 = 2`;
- upper endpoint: `(4/3)/2 = 2/3`;
- absolute gap: `4/3`.

The projective generator therefore cannot be constant on this response path.
This is a source-asymptotic D' failure even before the independent composition
requirement is tested.

## Why exact S-matrix composition does not close the scalar gate

The source's exact object is the phase- and momentum-dependent boundary S
matrix, while `G` is an integrated scalar observable. It supplies no binary
law `C(G1,G2)` for two conductance responses. The general distinction is
visible in an exact one-channel control: compose two identical lossless
50/50 scatterers with `t1=t2=1/sqrt(2)` and `r1=r2=i/sqrt(2)`. Exact serial
S-matrix composition gives

`T_total(phi) = 1/(5+4 cos(2 phi))`.

The same scalar inputs `T1=T2=1/2` yield `T_total(0)=1/9` but
`T_total(pi/2)=1`. A phase-blind binary scalar law therefore cannot reproduce
the exact composition.

This is consistent with the generalized-star-product theorem of Kostrykin and
Schrader, whose exact composition acts on full unitary scattering matrices
([arXiv](https://arxiv.org/abs/math-ph/0008022),
[JMP](https://doi.org/10.1063/1.1354641)). Ghoshal and Zamolodchikov provide
the exact factorizable boundary-S-matrix framework used by boundary
sine-Gordon theory
([arXiv](https://arxiv.org/abs/hep-th/9306002),
[IJMPA](https://doi.org/10.1142/S0217751X94001552)). Neither result defines a
closed binary law on the integrated conductance.

As a second control, exact factorized O(N) sigma-model amplitudes do combine at
the full multiparticle-operator level in a massive asymptotically free 1+1D
theory. That composition is likewise not a real scalar response law with the
marked Paper V boundaries, and it is not a four-dimensional quantum-gravity
candidate.

## Machine-readable result

Reproduce the frozen endpoint and scalar-composition gates with:

```bash
python scripts/paper5/dprime_external_ir_safe_composition_gate.py
python -m pytest tests/test_dprime_external_ir_safe_composition_gate.py -q
```

Artifact:

`results/paper5/DPRIME_EXTERNAL_IR_SAFE_COMPOSITION_GATE_2026-08-26.json`

## Verdict and claim boundary

The external search found one materially stronger near-candidate but zero
complete candidates. Its physical conductance has exact finite endpoints and
an exact nonperturbative scaling function, yet it fails D' through unequal
source endpoint limits and lacks a source-defined scalar binary composition.

No physical D' derivation, cosmology result, UV completion, RH result, or abc
result follows. Exact S-matrix composition is retained only as a control and
is not identified with the TBA-integrated conductance.

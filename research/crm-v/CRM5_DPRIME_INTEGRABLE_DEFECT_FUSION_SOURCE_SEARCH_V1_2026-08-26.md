# CRM5-DPRIME-INTEGRABLE-DEFECT-FUSION-SOURCE-SEARCH-V1

**Date:** 2026-08-26
**Scope:** One new primary-source family outside the local quadratic-gravity,
Bjorken, 2D Yang--Mills, FQHE, generic scattering, and massless-flow corpus
**Result:**
`EXACT_SOURCE_DEFINED_ISING_DEFECT_FUSION_DPRIME_SEMIGROUP__RG_RUNNING_AND_SIGNED_CHANNEL_NOT_SOURCE_DEFINED`

## Frozen source family and candidate

This search tested integrable line-defect fusion in two-dimensional Ising
field theory. The primary source is the 2026 preprint by He, Jiang, and Liu,
[Fusion of Integrable Defects and the Defect g-Function](https://arxiv.org/abs/2605.20688),
arXiv:2605.20688v1. It builds on the exact Ising line-defect scattering
solution of Delfino, Mussardo, and Simonetti,
[Scattering Theory and Correlation Functions in Statistical Models with a Line of Defect](https://arxiv.org/abs/hep-th/9409076)
([DOI](https://doi.org/10.1016/0550-3213(94)90032-9)). These papers form one
defect-scattering/fusion source family.

For the parity-invariant non-topological Ising defect, the exact transmission
and reflection amplitudes are

`T(theta, chi) = cos(chi) sinh(theta) / (sinh(theta) - i sin(chi))`,

`R(theta, chi) = i sin(chi) cosh(theta) / (sinh(theta) - i sin(chi))`,

with `chi = -2 arctan(g_I/2)` on the branch audited in the 2026 source. The
source restricts its discussion to positive `g_I`: negative coupling produces
a bound state, while `g_I=2` is purely reflective. At `g_I=0`, the exact
amplitudes reduce to `T=1`, `R=0`, the transparent neutral defect.

## Source-defined exact physical fusion

Fusion is not inferred from an algebraic reparametrization. The source defines
it physically as the short-distance limit `ma -> 0` of two defects. Summing
multiple reflections gives

`T_f = T_1 T_2 / (1 - R_1 R_2)`,

`R_f = R_1 + T_1^2 R_2 / (1 - R_1 R_2)`.

The fused amplitudes have exactly the same single-defect functional form at
the effective coupling

`g_I,f = (g_I,1 + g_I,2) / (1 + g_I,1 g_I,2 / 4)`.

Thus this family passes the physical-composition gate that blocked the
massless RG-flow amplitude audit.

## Exact projective semigroup control

Set `x=g_I/2`. On the source-audited positive branch, `0 <= x <= 1`, and the
fusion law becomes

`x_f = (x_1 + x_2) / (1 + x_1 x_2)`.

Therefore Paper V's marked quotient obeys the coefficient-free identity

`(1+x_f)/(1-x_f) = [(1+x_1)/(1-x_1)] [(1+x_2)/(1-x_2)]`,

or equivalently

`artanh(x_f) = artanh(x_1) + artanh(x_2)`.

This is an exact, source-defined D-prime algebra on a physical defect-fusion
semigroup. The computation also verifies directly that the multiple-scattering
amplitudes at `ma=0` equal the amplitudes of the single defect at `g_I,f`.

## Why physical Paper-V D-prime remains open

Three non-interchangeable gates remain open.

1. **Static coupling label versus scalar response.** The variable `x=g_I/2`
   is the defect-coupling label on which the exact fusion law closes. The
   source does not identify it with a running scalar observable. The physical
   reflection probability `p_R=|R(theta,g_I)|^2` has transparent and reflective
   endpoints, but its fusion is mediated through the full complex amplitudes;
   it does not inherit the same marked quotient as a scalar response.
2. **Positive semigroup versus signed reversible channel.** The audited source
   branch is `0 <= x <= 1`. Its neutral element `x=0` is the lower endpoint,
   not an interior mark between two source-audited response boundaries. The
   negative branch is expressly outside the source's discussion because it
   contains a bound state. Extending the algebra to `-1 < x < 1` would be an
   extra physical-domain claim, so this audit does not do it.
3. **Spatial fusion versus RG running.** The source's `ma` is the dimensionless
   defect separation, and `mR` is the finite-size TBA scale. It gives no beta
   function `g_I(mu)`, no map from additive RG time to repeated fusion, and no
   response homomorphism along a running trajectory. The source itself lists
   determining precisely when fusion can be interpreted as an RG flow as an
   open problem.

The exact composition is therefore retained as a stringent positive control,
while the frozen Paper-V contract still has zero complete physical candidates.

## Reproduction

```bash
python scripts/paper5/dprime_integrable_defect_fusion_gate.py
python -m pytest tests/test_dprime_integrable_defect_fusion_gate.py -q
```

Artifact:

`results/paper5/DPRIME_INTEGRABLE_DEFECT_FUSION_GATE_2026-08-26.json`

## Verdict and claim boundary

This single-family search establishes an exact physical defect-fusion law and
an exact projective positive-semigroup identity. It does not establish a
source-defined running scalar response, a full signed reversible response
interval, or a scale map `mu -> g_I(mu)`. No physical Paper-V D-prime
derivation, four-dimensional transfer, cosmology result, UV completion, RH
result, or abc result follows.

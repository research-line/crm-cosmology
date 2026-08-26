# CRM5-MONOTONICITY-LEMMA-GLOBAL-GROUP-V1

**Date:** 2026-08-26

**Result:** `GLOBAL_MONOTONICITY_SECURED__GLOBAL_HOMOMORPHISM_REQUIRED__NO_CIRCULAR_PROFILE_PREMISE`

## Scope

This bundle addresses CRM-V TODO lines 350--352 only: secure the monotonicity
lemma under a genuine global group structure and verify that the proof does
not assume monotonicity of the response profile `sigma`.

## Audit of the former corollary

The previous proof contained two gaps in scope:

1. it chose an additive control coordinate only "near the identity" but used
   the resulting derivative identity for every control value; and
2. it wrote `sigma'(0)=c_1`, although Axiom B defines `c_1` for the
   unnormalized response `S_T`, so `d sigma/dg(0)=c_1/S_max`.

The former wording also made Axiom C look redundant under the response-side
law `D^pm` alone. That is too strong: `D^pm` supplies a global group law on the
response interval, not a global homomorphism from the physical control
variable into that group.

## Secured lemma

Let `C` be a `C^1` group law on the connected interval `(-1,1)`, with every
translation `L_x(y)=C(x,y)` a `C^1` diffeomorphism. Let

```text
sigma : (R,+) -> ((-1,1),C)
```

be a global `C^1` homomorphism with `sigma(0)=0` and
`kappa=sigma'(0)>0`. Define the invariant generator

```text
a(x) = partial_2 C(x,0).
```

Then

```text
a(x) > 0,
sigma'(u) = kappa * a(sigma(u)) > 0  for every u in R.
```

The image of `sigma` is an open subgroup of the connected target group and
therefore the entire interval. Hence `sigma` is a strictly increasing
bijection and tends to the two response boundaries as `u` tends to plus or
minus infinity.

## Why the proof is not circular

The sign chain is independent of the response profile:

1. translation diffeomorphisms imply `a(x)` never vanishes;
2. connectedness and `a(0)=1` imply `a(x)>0` everywhere;
3. differentiating the global homomorphism identity at the second argument's
   identity gives the differential equation; and
4. only then is `sigma'(u)>0` concluded.

No prior monotonicity of `sigma`, no Abel coordinate, no Axiom C, and no
projective quotient D' occurs in those steps. The general equivalence between
a Lie-group homomorphism equation and its differential equation is also
treated directly by [Svetlichny (2009)](https://arxiv.org/abs/0912.4476); the
one-dimensional sign and open-subgroup argument used in Paper V is given
self-contained in the manuscript.

## Exact dependency boundary

| Item | Status |
|---|---|
| global response group on `(-1,1)` | required |
| global additive control group `(R,+)` | required |
| homomorphism identity for all `u,v` | required |
| positive orientation `kappa>0` | required |
| prior monotonicity of `sigma` | not used |
| projective D' | not used |
| single control direction | input, not derived |
| stochastic or multi-field control | out of scope |

Axiom B supplies `d sigma/dg(0)=c_1/S_max>0`. Its transfer to the global
additive coordinate additionally requires `du/dg(0)>0`. Consequently, the
monotonicity and endpoint-saturation clauses of Axiom C are redundant only in
this strengthened global, orientation-preserving, one-channel subclass.

## Negative and positive controls

- `sigma(u)=tanh(u+2 sin u)` is bounded, odd, saturating, and has positive
  local slope `sigma'(0)=3`, yet its derivative is negative near `u=pi`.
  It fails the global homomorphism gate and proves that local Axiom-B data do
  not imply global monotonicity.
- `sigma(u)=-tanh(u)` is a global homomorphism for the projective response law
  but has reversed orientation. It proves that `kappa>0` is necessary.
- The nonprojective collar
  `phi_epsilon(x)=atanh(x)+epsilon*x` has positive generator
  `a_epsilon(x)=(1-x^2)/(1+epsilon*(1-x^2))`. It verifies that the monotonicity
  lemma is independent of D'.

## Artifacts and reproduction

Machine-readable proof ledger:
`results/paper5/MONOTONICITY_LEMMA_GLOBAL_GROUP_2026-08-26.json`.

```bash
python -m pytest tests/test_global_monotonicity_lemma.py -q
cd papers/extensions
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
```

## Claim boundary

This audit proves a conditional mathematical dependency. It does not prove
that a specific quantum-gravity program supplies the global control
homomorphism, that a local RG chart extends globally, or that stochastic and
multi-field cosmologies satisfy Axiom C.

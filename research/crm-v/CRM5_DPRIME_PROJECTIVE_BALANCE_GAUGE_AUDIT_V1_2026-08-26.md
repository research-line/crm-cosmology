# CRM5-DPRIME-PROJECTIVE-BALANCE-GAUGE-AUDIT-V1

**Date:** 2026-08-26

**Result:** `CONDITIONAL_PROJECTIVE_CANONICALITY__PHYSICAL_SELECTION_OPEN__NO_CLAIM_UPGRADE`

## Scope

This bundle addresses CRM-V TODO lines 345--348 only: determine why
`R(x)=(1+x)/(1-x)` could be a natural response balance, and whether that
status is physical or merely a convenient coordinate gauge. It audits the
mathematical geometry separately from the missing source-bound physical law.

## Mathematical result: conditional projective canonicality

Mark the response interval by its lower boundary `b_minus=-1`, neutral
identity `e=0`, upper boundary `b_plus=1`, and an orientation. Then

```text
R(x) = ((x-b_minus)/(b_plus-x)) / ((e-b_minus)/(b_plus-e))
     = (1+x)/(1-x)
```

is the normalized four-point cross-ratio. Its logarithm

```text
h(x) = (1/2) log R(x) = atanh(x)
```

is the signed Hilbert coordinate from the neutral point. This is the precise
projective sense in which the quotient is natural. Hilbert geometry builds
its interval distance from a boundary cross-ratio; see
[Papadopoulos and Troyanov (2008)](https://arxiv.org/abs/0807.0335) and
[Rainio and Vuorinen (2023)](https://arxiv.org/abs/2303.03753).

The normalization needs every marked datum:

- A projective change of chart acting on the two boundaries, the neutral
  point, and `x` preserves the normalized four-point cross-ratio.
- If only the two boundaries are held fixed, the remaining one-parameter
  projective freedom has `R(T_k(x))=k R(x)`.
- Requiring the neutral point to remain `e=0` forces `k=1`.
- Reversing the interval orientation sends `R` to `1/R` and `h` to `-h`.

Thus a projective interval with the ordered marked triple `(-1,0,1)` selects
the quotient, up to the explicitly declared orientation. A bare smooth
interval does not.

## Category correction

The former manuscript sentence called the ratio itself an additive
work/rapidity coordinate. That was a multiplicative/additive category error:

```text
R(C(x,y)) = R(x) R(y)       multiplicative
h(C(x,y)) = h(x) + h(y)     additive, h=(1/2)log R
```

The bilingual manuscripts now state the correct distinction.

## Why generic response composition does not select R

For the smooth nonprojective family

```text
phi_epsilon(x) = atanh(x) + epsilon*x,
```

let `C_epsilon` be the composition induced by addition in `phi_epsilon`.
Then

```text
Q_epsilon(x) = exp(2 phi_epsilon(x))
             = R(x) exp(2 epsilon*x)
```

is exactly multiplicative under `C_epsilon`. The fixed cross-ratio `R` is
not: its D' defect is

```text
Delta_D' = -2 epsilon (C_epsilon(x,y)-x-y),
```

which is generally nonzero. Consequently, every admissible Abel group can be
given some multiplicative exponential coordinate. The non-trivial D' content
is the identification of that coordinate with the marked boundary
cross-ratio, not multiplicativity by itself.

## Physical selection gate

The projective construction becomes a physical response balance only if a
source independently supplies all of the following:

1. a gauge-invariant response observable;
2. two finite, distinguishable, predeclared boundary responses;
3. a source-defined neutral identity response;
4. an exact, independently sourced binary response composition; and
5. evidence that the signed Hilbert increments of this marked observable add.

Neither A--D nor `D^pm` supplies that projective marking. The current Paper V
evidence ledger also contains no physical candidate satisfying the exact
binary-law gate. The audit therefore does not upgrade D': it remains a
conditional projective gauge fixing and a measurable defect test.

## Artifacts and reproduction

Machine-readable audit:
`results/paper5/DPRIME_PROJECTIVE_BALANCE_GAUGE_AUDIT_2026-08-26.json`.

```bash
python -m pytest tests/test_dprime_projective_balance_gauge.py -q
cd papers/extensions
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
```

## Claim boundary

This audit proves a conditional mathematical naturality statement. It does
not establish that the CRM response, an RG coupling, or any quantum-gravity
observable carries the required marked projective structure. No physical D'
pass and no UV derivation is claimed.

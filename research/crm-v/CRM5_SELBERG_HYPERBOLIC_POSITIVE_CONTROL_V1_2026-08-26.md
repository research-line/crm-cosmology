# CRM5-SELBERG-HYPERBOLIC-POSITIVE-CONTROL-V1

**Date:** 2026-08-26

**Result:** `HYPERBOLIC_LIE_MOTIF_PASS__FULL_E10_TRANSFER_REJECTED__NO_COSMOLOGY_OR_DPRIME_CLAIM`

## Scope

This bundle addresses CRM-V TODO lines 358--373 only. It asks whether Selberg
provides a useful hyperbolic positive control, audits the old E10 table against
the actual CRM-V axioms, and fixes the boundary of any Lie-origin/saturation
embedding remark.

The TODO's historical source path
`.LAB/.ZETA-ZOO/FST_MATHEMATICS/selberg/` no longer exists. FileCommander
resolved the current source read-only at `.LAB/.ZETA-ZOO/CORE/selberg/`.
The source and CRM OneDrive trees both had active `cldflt.sys` high-risk status,
so no source project or OneDrive register was changed.

## Positive result: one shared rank-one Lie motif

The source-side Selberg structure is

```text
M = Gamma\H^2 = Gamma\PSL(2,R)/SO(2),
```

with a Laplace--Casimir operator that commutes with the spherical
bi-`K`-invariant convolution channel. The current Selberg proof note already
limits the statement to that channel; it explicitly rejects an automatic
intertwiner from individual geodesic-flow pullbacks to truncated interval
shifts. This is consistent with Selberg's original invariant-operator and
trace-formula setting:
[Selberg (1956)](https://cds.cern.ch/record/427143).

The CRM projective response law has a narrower Lie realization. For the boost
matrix

```text
B(u) = [[cosh u, sinh u],
        [sinh u, cosh u]],
```

one has `B(u)B(v)=B(u+v)`. Setting `x=tanh(u)` gives

```text
C(x,y) = tanh(atanh(x)+atanh(y)) = (x+y)/(1+x*y).
```

This is the collinear one-dimensional Einstein--Möbius law, a geodesic
one-parameter subgroup of rank-one hyperbolic geometry; see
[Ungar (2007)](https://doi.org/10.1016/j.camwa.2006.05.028).

The valid comparison is therefore precise but narrow: Selberg and the CRM
normal form both expose rank-one hyperbolic Lie structure. They do not use the
same state space, operator algebra, observable, or physical dynamics.

## E10 invariant audit

| CRM-V gate | Selberg source motif | Transfer result |
|---|---|---|
| A: finite response capacity | compactness or finite hyperbolic area | `CATEGORY_MISMATCH_NOT_ESTABLISHED` |
| B: cooperative reinforcement | Casimir centrality / Lie symmetry | `CATEGORY_MISMATCH_NOT_ESTABLISHED` |
| B': response oddness | antisymmetric Lie bracket | `CATEGORY_MISMATCH_NOT_ESTABLISHED` |
| C: monotone cosmic control | none | `OUT_OF_SCOPE_NOT_ESTABLISHED` |
| D: exact response composition | geodesic flow and spherical convolution compose | `SOURCE_SIDE_COMPOSITION_MOTIF_ONLY` |
| D^pm: reversible bounded response group | a one-parameter geodesic/boost subgroup exists | `SUBGROUP_MOTIF_ONLY` |
| D': physical projective quotient | rank-one hyperbolic geometry | `NOT_ESTABLISHED` |

The failures are not cosmetic missing citations:

- finite area is a measure of a surface, not a bound on a scalar response;
- Casimir commutation has no sign information for the CRM Taylor response;
- bracket antisymmetry is a bilinear algebra identity, not `S(-g)=-S(g)`;
- source-side composition becomes CRM Axiom D only after an explicit response
  homomorphism is supplied; and
- no Selberg observable marks two saturation boundaries and a neutral response.

Consequently the old idea-annex chain

```text
C2_X trivial <=> E10 satisfied <=> saturation embedding
```

is rejected. None of its two equivalences was proved, and the invariant audit
provides direct category mismatches for the proposed route.

## Admissible Paper V wording

Paper V may use Selberg as a **hyperbolic Lie-origin positive control** for one
question only: can a rank-one geometric setting possess a classical invariant
Casimir/operator channel? Selberg answers yes in its spherical convolution
sector. That fact does not verify CRM A--D/B', derive the `tanh` response,
select D', or turn the Selberg trace formula into a cosmological model.

The bilingual manuscripts now contain this bounded remark and explicitly state
the non-claims.

## Artifacts and reproduction

Machine-readable audit:
`results/paper5/SELBERG_HYPERBOLIC_POSITIVE_CONTROL_2026-08-26.json`.

```bash
python -m pytest tests/test_selberg_hyperbolic_positive_control.py -q
cd papers/extensions
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
```

## Claim boundary

This audit makes no statement about the excluded RH or abc projects, changes
neither source tree, and does not claim a cosmology, UV completion, physical
D', or stronger Saturation Theorem from Selberg geometry.

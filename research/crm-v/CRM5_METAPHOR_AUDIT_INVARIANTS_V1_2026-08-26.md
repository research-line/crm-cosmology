# CRM5-METAPHOR-AUDIT-INVARIANTS-V1

**Date:** 2026-08-26

**Result:** `METAPHOR_TRANSFER_AUDITED__NORMAL_FORM_STRUCTURAL_ONLY__NO_CLAIM_UPGRADE`

## Scope

This audit covers the six terms selected in the CRM-V TODO:
`saturation`, `ferromagnetic`, `cooperative`, `renormalization`,
`temperature`, and `capacity`. It also separates Paper V's conditional
Abel/collar equivalence from Wilsonian universality.

The TODO points to `.LAB/.PAPER-LINE/.PRIO-4/!!DRAFT__Metaphern/`. That path
was not present. The current source was resolved read-only at
`.TOPICS/.RESEARCH/.LAB/LLM/!!DRAFT__Metaphern/`. Its v4 methodology treats a
metaphor as a partial source-domain/target-domain mapping and explicitly warns
that a linguistic or classificatory mapping is not direct evidence for a
shared underlying structure.

## Decision rule

Paper V may use *structural* only when at least one of the following is shown:

1. an explicit normal-form map with stated preserved invariants; or
2. an explicit homomorphism that intertwines the source composition with the
   target response composition.

A common word, graph shape, finite endpoint, or occurrence of `tanh` is not
sufficient.

## Findings

| Transfer | Preserved | Missing | Status |
|---|---|---|---|
| saturation | bounded normalized interval, ordered endpoints, monotone endpoint approach | common microphysics or free energy | structural only at the response/normal-form level |
| ferromagnetic | signed scalar order parameter, mean-field `tanh` shape | magnetization composition, lattice correlations, critical exponents | heuristic analogy |
| cooperative | sign of the local response, `c_1 > 0` | interaction graph, many-body feedback, correlation function | local formal correspondence |
| renormalization | associativity only if an intertwining map exists | external theory-space-to-response homomorphism | conditional structural gate |
| temperature | order of a chosen one-dimensional control | units, thermal ensemble, conjugacy, identity with `a` | heuristic reparametrization |
| capacity | finite response endpoint | entropy, information, code, or holographic capacity | formal bound; physical reading heuristic |

The former sentence claiming that mean-field magnetization itself has an Abel
composition law was removed. Mean-field Ising magnetization satisfies a
self-consistency equation; a shared `tanh` shape does not define a binary
composition. Yang's exact two-dimensional magnetization and Wilson--Kogut RG
theory also make clear that critical behavior and universality are controlled
by scaling data and fixed-point structure, not by sharing a sigmoid.

## Manuscript changes

- EN is the lead language; DE was synchronized section-for-section.
- Paper V now states the explicit RG response-homomorphism criterion.
- The bilingual invariant table is embedded as
  `tab:metaphor_invariants`.
- Compatibility-map ratings were downgraded wherever only a source-domain
  motif, regulator bound, monotone segment, or coarse-graining operation was
  available.
- Unsupported claims about ferromagnetic composition, vacuum analyticity,
  automatic cooperation, and automatic transfer from theory-space RG were
  removed.
- Paper V's universality is now named a conditional Abel/collar equivalence
  class, not a Wilsonian universality class.

## Evidence

- C. N. Yang, *The Spontaneous Magnetization of a Two-Dimensional Ising
  Model*, Physical Review 85 (1952), DOI
  [10.1103/PhysRev.85.808](https://doi.org/10.1103/PhysRev.85.808).
- K. G. Wilson and J. Kogut, *The Renormalization Group and the Epsilon
  Expansion*, Physics Reports 12 (1974), DOI
  [10.1016/0370-1573(74)90023-4](https://doi.org/10.1016/0370-1573(74)90023-4).
- G. Lakoff, *Explaining Embodied Cognition Results*, Topics in Cognitive
  Science 4 (2012), DOI
  [10.1111/j.1756-8765.2012.01222.x](https://doi.org/10.1111/j.1756-8765.2012.01222.x).

## Reproduction

```bash
python -m pytest tests/test_metaphor_transfer_invariants.py -q
cd papers/extensions
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_EN.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
pdflatex -interaction=nonstopmode -halt-on-error Paper5_DE.tex
```

Machine-readable audit:
`results/paper5/METAPHOR_TRANSFER_INVARIANTS_2026-08-26.json`.

## Claim boundary

This audit narrows language and records missing maps. It does not derive an
external QG response homomorphism, establish a Wilsonian universality class,
identify temperature with the scale factor, infer spin-like microphysics, or
close physical D'.

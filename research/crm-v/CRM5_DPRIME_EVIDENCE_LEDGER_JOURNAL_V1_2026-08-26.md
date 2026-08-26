# CRM5-DPRIME-EVIDENCE-LEDGER-JOURNAL-V1

**Date:** 2026-08-26
**Scope:** Machine-readable journal ledger for the Paper V projective-boundary
condition D'
**Result:** `JOURNAL_LEDGER_COMPLETE__PHYSICAL_DPRIME_OPEN`

## Question

Can the 2026-06-21 residual prototype and all subsequent source-bound D'
checks be represented in one journal-ready ledger without promoting a control,
model result, or mathematical reparametrization into a physical D' derivation?

## Frozen schema

Every entry contains the selector-requested fields

`target | evidence_source | model_dependency | preregistered_controls | status`

and the diagnostic fields `target_type`, `dprime_outcome`,
`composition_status`, `boundary_status`, `scale_status`, `metric`,
`result_artifact`, and `claim_pass`. The JSON Schema fixes the admissible status
vocabulary and requires `claim_pass` to be false. A metric that could not be
evaluated is encoded as JSON `null`, never as numerical zero.

## Coverage

The deterministic builder freezes 13 unique entries:

- 7 rows migrated from the 2026-06-21 prototype: two analytic projective
  controls, four nonprojective collar controls, and one synthetic RG-scale
  composition control;
- 6 later source candidates: Agravity/QED photon scattering, the Bjorken
  effective charge, exact two-dimensional U(1) Yang--Mills, the standard LQA
  large-N `xi` projection, its log-log reparametrization, and the complete LQA
  `(lambda, xi)` trajectory followed by the tensor-`r` projection;
- 10 registered evidence sources, including 8 external primary sources.

The outcome classes are deliberately disjoint: 2 analytic control passes,
4 analytic control failures, 1 synthetic nonphysical pass, 1 not-decidable
source candidate, 4 model-bound failures, and 1 mathematical
reparametrization pass that is not physical time.

## Evidence binding

Each source candidate cites at least one registered primary source. The ledger
uses the source papers only for the claims they actually support: gauge-fixing
independence and scattering limits; observable effective-charge behavior and
commensurate-scale transitivity; the analytic effective-charge model; exact
two-dimensional Yang--Mills heat-kernel/Wilson-loop structure; and the quoted
large-N quadratic-gravity trajectory. Current local 2D Yang--Mills and full
two-coupling LQA result JSON files are loaded by the builder, and a status drift
causes generation to fail.

This evidence does not provide the missing source-exact physical binary
response composition for Paper V. Consequently all 13 `claim_pass` values are
false and `physical_dprime_closed` remains false.

## Reproduction

```bash
python scripts/paper5/build_dprime_evidence_ledger.py
python -m pytest tests/test_dprime_evidence_ledger_journal.py -q
```

Generated artifacts:

- `results/paper5/DPRIME_EVIDENCE_LEDGER_JOURNAL_SCHEMA_V1.json`
- `results/paper5/DPRIME_EVIDENCE_LEDGER_JOURNAL_2026-08-26.json`
- `results/paper5/DPRIME_EVIDENCE_LEDGER_JOURNAL_2026-08-26.csv`
- `results/paper5/DPRIME_EVIDENCE_LEDGER_JOURNAL_2026-08-26.md`

## Claim boundary

The ledger closes the journal-format and evidence-traceability task only. It
does not close physical D', establish a microscopic derivation, transfer the
exact 2D Yang--Mills response to four-dimensional scattering or RG evolution,
or upgrade any Paper V or CRM claim.

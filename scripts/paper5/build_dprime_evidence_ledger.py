"""Build the source-bound CRM-V D-prime journal evidence ledger.

The ledger migrates the seven analytic prototype rows from June 2026 and
adds every subsequently executed candidate gate that has a stable result.
Its five selector-mandated fields are first-class schema requirements:
``target``, ``evidence_source``, ``model_dependency``,
``preregistered_controls``, and ``status``.

Model-bound failures, mathematical controls, and source-incomplete candidates
remain distinct.  No row is allowed to turn an unavailable metric into zero
or to promote a control/model result to a physical Paper V claim.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


LEDGER_ID = "CRM5-DPRIME-EVIDENCE-LEDGER-JOURNAL-V1"
RUN_DATE = "2026-08-26"
SCHEMA_VERSION = "1.0.0"
ARTIFACT_STEM = "DPRIME_EVIDENCE_LEDGER_JOURNAL_2026-08-26"
SCHEMA_FILENAME = "DPRIME_EVIDENCE_LEDGER_JOURNAL_SCHEMA_V1.json"
REQUIRED_FIELDS = (
    "target",
    "evidence_source",
    "model_dependency",
    "preregistered_controls",
    "status",
)

STATUS_VOCABULARY = (
    "CONTROL_PASS_PROJECTIVE",
    "CONTROL_FAIL_PROJECTIVE",
    "SYNTHETIC_SCALE_COMPOSITION_PASS__NOT_PHYSICAL",
    "NOT_DECIDABLE_SOURCE_INCOMPLETE",
    "MODEL_BOUND_DPRIME_FAIL__PHYSICAL_C_NOT_SOURCE_EXACT",
    "EXACT_GAUGE_RESPONSE_COMPOSITION__DPRIME_FAIL__NOT_4D_SCATTERING_OR_RG",
    "MODEL_BOUND_DPRIME_FAIL__SOURCE_PHYSICS_DEBATED",
    "MATHEMATICAL_REPARAMETRIZATION_PASS__NOT_PHYSICAL_TIME",
    "FULL_2D_LARGE_N_TRAJECTORY__R_PROJECTION_DPRIME_FAIL__NO_EXACT_C",
)

TARGET_TYPES = ("analytic_control", "synthetic_control", "source_candidate")
DPRIME_OUTCOMES = (
    "pass_control",
    "fail_control",
    "pass_synthetic_not_physical",
    "fail_model_bound",
    "pass_reparametrization_not_physical",
    "not_decidable",
)

SOURCE_REGISTRY = {
    "CRM5_RESIDUAL_LEDGER_2026": {
        "kind": "internal_analytic",
        "citation": "CRM-V D-prime Residual Ledger, proof note and results (2026-06-21)",
        "url": "",
        "locator": "legacy-onedrive://CRM-V/DPRIME_RESIDUAL_LEDGER_2026-06-21",
        "verified_date": RUN_DATE,
    },
    "CRM5_GENERATOR_LEDGER_2026": {
        "kind": "internal_analytic",
        "citation": "CRM-V D-prime RG generator equivalence audit (2026-08-08)",
        "url": "",
        "locator": "legacy-onedrive://CRM-V/DPRIME_RG_GENERATOR_EQUIVALENCE_2026-08-08",
        "verified_date": RUN_DATE,
    },
    "CUNHA_LEHUM_2026": {
        "kind": "external_primary",
        "citation": "Cunha and Lehum, Scattering amplitudes in dimensionless quadratic gravity coupled to QED (2026)",
        "url": "https://doi.org/10.1103/k79x-52gj",
        "arxiv": "https://arxiv.org/abs/2603.05476",
        "locator": "Eqs. (17)-(19); gauge-fixing and forward/backward limits",
        "verified_date": RUN_DATE,
    },
    "DEUR_ET_AL_2022": {
        "kind": "external_primary",
        "citation": "Deur et al., Experimental determination of the QCD effective charge alpha_g1(Q), Particles 5, 171 (2022)",
        "url": "https://doi.org/10.3390/particles5020015",
        "arxiv": "https://arxiv.org/abs/2205.01169",
        "locator": "effective-charge definition and measured low-Q behavior",
        "verified_date": RUN_DATE,
    },
    "BRODSKY_LU_1995": {
        "kind": "external_primary",
        "citation": "Brodsky and Lu, Commensurate Scale Relations in Quantum Chromodynamics, Physical Review D 51, 3652 (1995)",
        "url": "https://doi.org/10.1103/PhysRevD.51.3652",
        "arxiv": "https://arxiv.org/abs/hep-ph/9405218",
        "locator": "renormalization-group transitivity for commensurate scales",
        "verified_date": RUN_DATE,
    },
    "DE_TERAMOND_ET_AL_2024": {
        "kind": "external_primary",
        "citation": "de Teramond et al., The strong coupling in the nonperturbative and near-perturbative regimes (2024)",
        "url": "https://arxiv.org/abs/2403.16126",
        "locator": "Eqs. (1), (4)-(6), analytic effective-charge model and beta function",
        "verified_date": RUN_DATE,
    },
    "AROCA_KUBYSHIN_2000": {
        "kind": "external_primary",
        "citation": "Aroca and Kubyshin, Study of Wilson loop functionals in 2D Yang-Mills theories, Annals of Physics 283 (2000)",
        "url": "https://doi.org/10.1006/aphy.2000.6044",
        "arxiv": "https://arxiv.org/abs/hep-th/9901155",
        "locator": "heat-kernel formulation and U(1) plane area law, Eq. (62)",
        "verified_date": RUN_DATE,
    },
    "WITTEN_1991": {
        "kind": "external_primary",
        "citation": "Witten, On quantum gauge theories in two dimensions, Communications in Mathematical Physics 141 (1991)",
        "url": "https://doi.org/10.1007/BF02100009",
        "locator": "gauge-invariant Wilson-line framework",
        "verified_date": RUN_DATE,
    },
    "NGUYEN_2018": {
        "kind": "external_primary",
        "citation": "Nguyen, Quantum Yang-Mills theory in two dimensions: exact versus perturbative, Communications in Mathematical Physics 357 (2018)",
        "url": "https://doi.org/10.1007/s00220-017-2942-6",
        "arxiv": "https://arxiv.org/abs/1508.06305",
        "locator": "continuum Wilson-loop construction via group heat kernels",
        "verified_date": RUN_DATE,
    },
    "LIU_QUINTIN_AFSHORDI_2026": {
        "kind": "external_primary",
        "citation": "Liu, Quintin, and Afshordi, Ultraviolet Completion of the Big Bang in Quadratic Gravity, Physical Review Letters 136, 111501 (2026)",
        "url": "https://doi.org/10.1103/6gtx-j455",
        "arxiv": "https://arxiv.org/abs/2510.18733",
        "locator": "main Eq. (2); Supplemental Eqs. (9), (22)-(26)",
        "verified_date": RUN_DATE,
    },
}

LEGACY_RESIDUAL_CASES = (
    ("canonical_arctanh", "CONTROL_PASS_PROJECTIVE", "pass_control", 1.8962609260597674e-12),
    ("scaled_2_arctanh", "CONTROL_PASS_PROJECTIVE", "pass_control", 1.8962609260597674e-12),
    ("collar_eps_plus_0.05", "CONTROL_FAIL_PROJECTIVE", "fail_control", 0.09012008846000352),
    ("collar_eps_plus_0.10", "CONTROL_FAIL_PROJECTIVE", "fail_control", 0.18021949471456633),
    ("collar_eps_minus_0.05", "CONTROL_FAIL_PROJECTIVE", "fail_control", 0.09014379288085905),
    ("collar_cubic_plus_0.05", "CONTROL_FAIL_PROJECTIVE", "fail_control", 0.07184145847414047),
)


@dataclass(frozen=True)
class LedgerEntry:
    target: str
    evidence_source: list[str]
    model_dependency: str
    preregistered_controls: list[str]
    status: str
    target_type: str
    dprime_outcome: str
    composition_status: str
    boundary_status: str
    scale_status: str
    metric: dict[str, object]
    result_artifact: str
    claim_pass: bool = False


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"missing evidence artifact: {path}")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"evidence artifact is not an object: {path}")
    return loaded


def _legacy_entries() -> list[LedgerEntry]:
    entries = []
    for target, status, outcome, max_abs_delta in LEGACY_RESIDUAL_CASES:
        dependency = (
            "none__analytic_projective_abel_coordinate"
            if "arctanh" in target
            else "none__analytic_smooth_nonprojective_collar"
        )
        entries.append(
            LedgerEntry(
                target=target,
                evidence_source=["CRM5_RESIDUAL_LEDGER_2026"],
                model_dependency=dependency,
                preregistered_controls=[
                    "positive_face_grid_x_y_0.05_to_0.95",
                    "fixed_projective_quotient_R",
                    "common_delta_threshold",
                ],
                status=status,
                target_type="analytic_control",
                dprime_outcome=outcome,
                composition_status="exact_internal_abel_composition",
                boundary_status="synthetic_fixed_open_interval",
                scale_status="not_physical_scale",
                metric={"name": "max_abs_delta", "value": max_abs_delta},
                result_artifact=(
                    "legacy-onedrive://CRM-V/_results/"
                    "DPRIME_RESIDUAL_LEDGER_2026-06-21.json"
                ),
            )
        )
    entries.append(
        LedgerEntry(
            target="rg_scale_ratio_tanh_k1",
            evidence_source=["CRM5_RESIDUAL_LEDGER_2026"],
            model_dependency="synthetic_tanh_response_on_multiplicative_scale_semigroup",
            preregistered_controls=[
                "same_delta_threshold_as_collar_controls",
                "r_grid_1.05_to_10",
                "k_equals_1",
            ],
            status="SYNTHETIC_SCALE_COMPOSITION_PASS__NOT_PHYSICAL",
            target_type="synthetic_control",
            dprime_outcome="pass_synthetic_not_physical",
            composition_status="exact_scale_semigroup__synthetic_response",
            boundary_status="synthetic_projective_anchors",
            scale_status="multiplicative_rg_scale_only",
            metric={"name": "max_abs_delta", "value": 1.652011860642233e-13},
            result_artifact=(
                "legacy-onedrive://CRM-V/_results/"
                "DPRIME_RESIDUAL_LEDGER_2026-06-21.json"
            ),
        )
    )
    return entries


def build_entries(repo_root: Path | None = None) -> list[LedgerEntry]:
    root = repo_root or _repo_root()
    ym_path = root / "results" / "paper5" / "DPRIME_2D_YM_HEAT_KERNEL_GATE_2026-08-26.json"
    lqa_path = root / "results" / "paper5" / "DPRIME_LQA_2D_TRAJECTORY_RPROJ_GATE_2026-08-26.json"
    ym = _read_json(ym_path)
    lqa = _read_json(lqa_path)

    if ym["status"] != "EXACT_GAUGE_RESPONSE_COMPOSITION__DPRIME_FAIL__NOT_4D_SCATTERING_OR_RG":
        raise ValueError("2D Yang-Mills evidence status drifted")
    if lqa["status"] != "FULL_2D_LARGE_N_TRAJECTORY__R_PROJECTION_DPRIME_FAIL__NO_EXACT_C":
        raise ValueError("LQA two-coupling evidence status drifted")

    entries = _legacy_entries()
    entries.extend(
        [
            LedgerEntry(
                target="agravity_qed_gamma_gamma_unpolarized_sqamp_tree",
                evidence_source=["CUNHA_LEHUM_2026"],
                model_dependency="massless_tree_level_one_graviton_exchange_fixed_couplings",
                preregistered_controls=[
                    "canonical_arctanh",
                    "collar_cubic_plus_0.05",
                    "natural_forward_and_backward_angle_anchors",
                ],
                status="NOT_DECIDABLE_SOURCE_INCOMPLETE",
                target_type="source_candidate",
                dprime_outcome="not_decidable",
                composition_status="not_source_defined",
                boundary_status="degenerate__both_natural_responses_diverge_to_plus_infinity",
                scale_status="tree_level_fixed_couplings__running_deferred_by_source",
                metric={
                    "name": "dprime_metric",
                    "value": None,
                    "reason": "boundary_pair_degenerate_and_composition_missing",
                },
                result_artifact=(
                    "legacy-onedrive://CRM-V/_proof-notes/"
                    "CRM5_DPRIME_PHYS_OBS_V1_2026-08-24.md"
                ),
            ),
            LedgerEntry(
                target="bjorken_effective_charge_alpha_g1",
                evidence_source=[
                    "DEUR_ET_AL_2022",
                    "BRODSKY_LU_1995",
                    "DE_TERAMOND_ET_AL_2024",
                ],
                model_dependency="physical_effective_charge_plus_de_teramond_analytic_model",
                preregistered_controls=[
                    "fixed_GDH_and_asymptotic_freedom_anchors",
                    "canonical_tanh_generator_positive_control",
                    "eleven_Q_values_0.001_to_100_GeV",
                ],
                status="MODEL_BOUND_DPRIME_FAIL__PHYSICAL_C_NOT_SOURCE_EXACT",
                target_type="source_candidate",
                dprime_outcome="fail_model_bound",
                composition_status="CSR_transitivity_supported__exact_response_C_not_source_defined",
                boundary_status="physical_finite_distinct__alpha_g1_0_pi__alpha_g1_infinity_0",
                scale_status="additive_log_Q_squared__model_validity_limited_in_full_UV",
                metric={
                    "name": "projective_generator_limits",
                    "ir_limit": 0.5,
                    "uv_limit": 0.0,
                    "grid_span": 0.558359378671,
                },
                result_artifact=(
                    "legacy-onedrive://CRM-V/_proof-notes/"
                    "CRM5_DPRIME_BJORKEN_EFFECTIVE_CHARGE_V1_2026-08-26.md"
                ),
            ),
            LedgerEntry(
                target="u1_2d_yang_mills_wilson_loop_area_response",
                evidence_source=[
                    "AROCA_KUBYSHIN_2000",
                    "WITTEN_1991",
                    "NGUYEN_2018",
                ],
                model_dependency="exact_pure_2d_U1_Yang_Mills_heat_kernel_area_law",
                preregistered_controls=[
                    "exact_semigroup_identity",
                    "normalized_composition_associativity",
                    "two_finite_response_boundaries",
                ],
                status=str(ym["status"]),
                target_type="source_candidate",
                dprime_outcome="fail_model_bound",
                composition_status="exact_source_response_composition",
                boundary_status="finite_distinct_response_values__minus_1_plus_1",
                scale_status="additive_area__not_4d_scattering_or_rg_time",
                metric={
                    "name": "projective_generator_witness",
                    "at_x_0": ym["dprime_witness"]["at_x_0"],
                    "at_x_0_5": ym["dprime_witness"]["at_x_0_5"],
                },
                result_artifact="results/paper5/DPRIME_2D_YM_HEAT_KERNEL_GATE_2026-08-26.json",
            ),
            LedgerEntry(
                target="lqa_largeN_xi_in_log_mu",
                evidence_source=[
                    "LIU_QUINTIN_AFSHORDI_2026",
                    "CRM5_GENERATOR_LEDGER_2026",
                ],
                model_dependency="large_N_one_loop_xi_projection__debated_physical_beta_functions",
                preregistered_controls=[
                    "logistic_tanh_positive_control",
                    "cubic_abel_warp_negative_control",
                    "fixed_t_equals_log_mu_over_mu0",
                ],
                status="MODEL_BOUND_DPRIME_FAIL__SOURCE_PHYSICS_DEBATED",
                target_type="source_candidate",
                dprime_outcome="fail_model_bound",
                composition_status="RG_flow_only__no_exact_physical_response_C",
                boundary_status="model_normalized_finite_asymptotic_anchors",
                scale_status="standard_additive_log_mu__source_physics_debated",
                metric={
                    "name": "generator_and_stationarity",
                    "generator_residual": 1.344,
                    "stationarity_span": 1.492,
                },
                result_artifact=(
                    "legacy-onedrive://CRM-V/_results/"
                    "DPRIME_RG_GENERATOR_GATE_2026-08-08.json"
                ),
            ),
            LedgerEntry(
                target="lqa_largeN_xi_in_log_log_mu",
                evidence_source=[
                    "LIU_QUINTIN_AFSHORDI_2026",
                    "CRM5_GENERATOR_LEDGER_2026",
                ],
                model_dependency="same_large_N_xi_path__second_logarithm_reparametrization",
                preregistered_controls=[
                    "same_source_path_as_standard_time_fail",
                    "tau_equals_log_log_mu_over_mu0",
                    "physical_time_justification_required",
                ],
                status="MATHEMATICAL_REPARAMETRIZATION_PASS__NOT_PHYSICAL_TIME",
                target_type="source_candidate",
                dprime_outcome="pass_reparametrization_not_physical",
                composition_status="mathematical_linearization_only__no_physical_C",
                boundary_status="model_normalized_finite_asymptotic_anchors",
                scale_status="unjustified_second_logarithm__not_physical_time",
                metric={
                    "name": "generator_residual",
                    "value": 1.67e-16,
                    "stationarity_span": 1.33e-15,
                },
                result_artifact=(
                    "legacy-onedrive://CRM-V/_results/"
                    "DPRIME_RG_GENERATOR_GATE_2026-08-08.json"
                ),
            ),
            LedgerEntry(
                target="lqa_full_lambda_xi_trajectory_tensor_r_projection",
                evidence_source=["LIU_QUINTIN_AFSHORDI_2026"],
                model_dependency="preregistered_large_N_two_coupling_path_plus_FLRW_tensor_r_projection",
                preregistered_controls=[
                    "two_coordinate_retention",
                    "reduced_and_full_beta_residuals",
                    "six_frozen_b_Nm_cases",
                    "source_tensor_r_anchor",
                ],
                status=str(lqa["status"]),
                target_type="source_candidate",
                dprime_outcome="fail_model_bound",
                composition_status="not_source_defined__rank_one_FLRW_projection",
                boundary_status="model_finite_distinct__r_16_to_0",
                scale_status="log_mu_with_ambiguous_curvature_scale_map",
                metric={
                    "name": "dprime_relative_spread",
                    "minimum": min(
                        row["dprime_relative_spread"]
                        for row in lqa["case_summaries"]
                    ),
                    "maximum": max(
                        row["dprime_relative_spread"]
                        for row in lqa["case_summaries"]
                    ),
                    "max_full_beta_residual": lqa["maxima"]["full_vector_residual"],
                },
                result_artifact=(
                    "results/paper5/"
                    "DPRIME_LQA_2D_TRAJECTORY_RPROJ_GATE_2026-08-26.json"
                ),
            ),
        ]
    )
    return entries


def build_json_schema() -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/research-line/crm-cosmology/results/paper5/DPRIME_EVIDENCE_LEDGER_JOURNAL_SCHEMA_V1.json",
        "title": "CRM-V D-prime journal evidence ledger entry",
        "type": "object",
        "required": list(REQUIRED_FIELDS),
        "properties": {
            "target": {"type": "string", "minLength": 1},
            "evidence_source": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
                "minItems": 1,
                "uniqueItems": True,
            },
            "model_dependency": {"type": "string", "minLength": 1},
            "preregistered_controls": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
                "minItems": 1,
                "uniqueItems": True,
            },
            "status": {"type": "string", "enum": list(STATUS_VOCABULARY)},
            "target_type": {"type": "string", "enum": list(TARGET_TYPES)},
            "dprime_outcome": {"type": "string", "enum": list(DPRIME_OUTCOMES)},
            "composition_status": {"type": "string", "minLength": 1},
            "boundary_status": {"type": "string", "minLength": 1},
            "scale_status": {"type": "string", "minLength": 1},
            "metric": {"type": "object"},
            "result_artifact": {"type": "string", "minLength": 1},
            "claim_pass": {"const": False},
        },
        "additionalProperties": False,
    }


def validate_entries(
    entries: list[LedgerEntry],
    repo_root: Path | None = None,
) -> list[str]:
    root = repo_root or _repo_root()
    errors: list[str] = []
    targets = [entry.target for entry in entries]
    if len(targets) != len(set(targets)):
        errors.append("targets must be unique")

    for entry in entries:
        record = asdict(entry)
        for field in REQUIRED_FIELDS:
            value = record[field]
            if value is None or value == "" or value == []:
                errors.append(f"{entry.target}: required field {field} is empty")
        if entry.status not in STATUS_VOCABULARY:
            errors.append(f"{entry.target}: unknown status {entry.status}")
        if entry.target_type not in TARGET_TYPES:
            errors.append(f"{entry.target}: unknown target_type {entry.target_type}")
        if entry.dprime_outcome not in DPRIME_OUTCOMES:
            errors.append(f"{entry.target}: unknown dprime_outcome {entry.dprime_outcome}")
        if entry.claim_pass:
            errors.append(f"{entry.target}: journal control/candidate cannot claim pass")
        missing_sources = [
            source_id
            for source_id in entry.evidence_source
            if source_id not in SOURCE_REGISTRY
        ]
        if missing_sources:
            errors.append(f"{entry.target}: unknown sources {missing_sources}")
        if entry.target_type == "source_candidate" and not any(
            SOURCE_REGISTRY.get(source_id, {}).get("kind") == "external_primary"
            for source_id in entry.evidence_source
        ):
            errors.append(f"{entry.target}: source candidate lacks a primary source")
        if entry.dprime_outcome == "not_decidable" and entry.metric.get("value") is not None:
            errors.append(f"{entry.target}: unavailable D-prime metric must remain null")
        if entry.result_artifact.startswith(("results/", "research/")):
            if not (root / entry.result_artifact).is_file():
                errors.append(f"{entry.target}: missing local artifact {entry.result_artifact}")

    for source_id, source in SOURCE_REGISTRY.items():
        if source["kind"] == "external_primary":
            url = str(source["url"])
            if not url.startswith("https://"):
                errors.append(f"{source_id}: primary URL must be HTTPS")
            if "search" in url.lower():
                errors.append(f"{source_id}: search-result URLs are not admissible")
    return errors


def build_ledger(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or _repo_root()
    entries = build_entries(root)
    errors = validate_entries(entries, root)
    if errors:
        raise ValueError("ledger validation failed: " + "; ".join(errors))
    records = [asdict(entry) for entry in entries]
    status_counts = Counter(entry.status for entry in entries)
    outcome_counts = Counter(entry.dprime_outcome for entry in entries)
    return {
        "ledger_id": LEDGER_ID,
        "schema_version": SCHEMA_VERSION,
        "run_date": RUN_DATE,
        "required_fields": list(REQUIRED_FIELDS),
        "source_registry": SOURCE_REGISTRY,
        "entries": records,
        "summary": {
            "entry_count": len(entries),
            "prototype_rows_migrated": len(LEGACY_RESIDUAL_CASES) + 1,
            "source_candidate_count": sum(
                entry.target_type == "source_candidate" for entry in entries
            ),
            "external_primary_source_count": sum(
                source["kind"] == "external_primary"
                for source in SOURCE_REGISTRY.values()
            ),
            "status_counts": dict(sorted(status_counts.items())),
            "outcome_counts": dict(sorted(outcome_counts.items())),
            "physical_claim_pass_count": sum(entry.claim_pass for entry in entries),
            "physical_dprime_closed": False,
        },
        "claim_boundary": [
            "Control passes are not physical D-prime derivations.",
            "Model-bound failures are not no-go theorems for the physical observable.",
            "Null metrics mean not evaluable and are never encoded as zero.",
            "Every source candidate has at least one registered primary source.",
            "No Paper V or CRM claim is upgraded.",
        ],
    }


def _write_text(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def _csv_rows(ledger: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for entry in ledger["entries"]:
        row = dict(entry)
        row["evidence_source"] = json.dumps(
            row["evidence_source"], ensure_ascii=False, separators=(",", ":")
        )
        row["preregistered_controls"] = json.dumps(
            row["preregistered_controls"], ensure_ascii=False, separators=(",", ":")
        )
        row["metric"] = json.dumps(
            row["metric"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        row["claim_pass"] = json.dumps(row["claim_pass"])
        rows.append(row)
    return rows


def _markdown_report(ledger: dict[str, object]) -> str:
    summary = ledger["summary"]
    lines = [
        "# CRM-V D-prime journal evidence ledger",
        "",
        f"- Ledger: `{ledger['ledger_id']}`",
        f"- Schema: `{ledger['schema_version']}`",
        f"- Entries: `{summary['entry_count']}`",
        f"- Migrated prototype rows: `{summary['prototype_rows_migrated']}`",
        f"- Source candidates: `{summary['source_candidate_count']}`",
        f"- Physical claim passes: `{summary['physical_claim_pass_count']}`",
        "",
        "## Required journal fields",
        "",
        "`target | evidence_source | model_dependency | preregistered_controls | status`",
        "",
        "## Entries",
        "",
        "| Target | Evidence source IDs | Model dependency | Preregistered controls | Status | D' outcome |",
        "|---|---|---|---|---|---|",
    ]
    for entry in ledger["entries"]:
        lines.append(
            "| `{target}` | `{sources}` | `{model_dependency}` | `{controls}` | `{status}` | `{dprime_outcome}` |".format(
                target=entry["target"],
                sources="; ".join(entry["evidence_source"]),
                model_dependency=entry["model_dependency"],
                controls="; ".join(entry["preregistered_controls"]),
                status=entry["status"],
                dprime_outcome=entry["dprime_outcome"],
            )
        )
    lines.extend(["", "## Source registry", "", "| ID | Kind | Citation | Locator |", "|---|---|---|---|"])
    for source_id, source in ledger["source_registry"].items():
        citation = source["citation"]
        if source["url"]:
            citation = f"[{citation}]({source['url']})"
        lines.append(
            f"| `{source_id}` | `{source['kind']}` | {citation} | {source['locator']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation guard",
            "",
            "The ledger keeps analytic controls, synthetic scale laws, source-incomplete",
            "candidates, model-bound failures, and mathematical reparametrizations in",
            "different status classes. A null metric means that D' was not evaluable; it",
            "is not a numerical zero. Every physical/model candidate cites at least one",
            "primary source, yet no row supplies the still-missing source-exact physical",
            "binary response composition needed to close Paper V's physical D' gate.",
            "",
        ]
    )
    return "\n".join(lines)


def write_artifacts(output_dir: Path, repo_root: Path | None = None) -> list[Path]:
    ledger = build_ledger(repo_root)
    schema = build_json_schema()
    output_dir.mkdir(parents=True, exist_ok=True)
    schema_path = output_dir / SCHEMA_FILENAME
    json_path = output_dir / f"{ARTIFACT_STEM}.json"
    csv_path = output_dir / f"{ARTIFACT_STEM}.csv"
    md_path = output_dir / f"{ARTIFACT_STEM}.md"

    _write_text(schema_path, json.dumps(schema, indent=2, sort_keys=True) + "\n")
    _write_text(json_path, json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    rows = _csv_rows(ledger)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    _write_text(md_path, _markdown_report(ledger))
    return [schema_path, json_path, csv_path, md_path]


def _default_output_dir() -> Path:
    return _repo_root() / "results" / "paper5"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=_default_output_dir())
    args = parser.parse_args(argv)
    paths = write_artifacts(args.output_dir)
    ledger = build_ledger()
    print(
        f"{ledger['ledger_id']} entries={ledger['summary']['entry_count']} "
        f"physical_claim_passes={ledger['summary']['physical_claim_pass_count']}"
    )
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

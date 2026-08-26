import csv
import json
import subprocess
import sys
from pathlib import Path

from scripts.paper5.build_dprime_evidence_ledger import (
    ARTIFACT_STEM,
    LEGACY_RESIDUAL_CASES,
    REQUIRED_FIELDS,
    SCHEMA_FILENAME,
    SOURCE_REGISTRY,
    STATUS_VOCABULARY,
    build_entries,
    build_json_schema,
    build_ledger,
    validate_entries,
    write_artifacts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "build_dprime_evidence_ledger.py"


def test_schema_requires_exact_selector_fields():
    schema = build_json_schema()

    assert schema["required"] == list(REQUIRED_FIELDS)
    assert schema["properties"]["status"]["enum"] == list(STATUS_VOCABULARY)
    assert schema["properties"]["claim_pass"] == {"const": False}


def test_ledger_migrates_every_prototype_row_and_all_later_candidates():
    ledger = build_ledger(REPO_ROOT)
    targets = {entry["target"] for entry in ledger["entries"]}

    assert ledger["summary"]["prototype_rows_migrated"] == len(LEGACY_RESIDUAL_CASES) + 1
    assert ledger["summary"]["entry_count"] == 14
    assert {
        "canonical_arctanh",
        "scaled_2_arctanh",
        "collar_eps_plus_0.05",
        "collar_eps_plus_0.10",
        "collar_eps_minus_0.05",
        "collar_cubic_plus_0.05",
        "rg_scale_ratio_tanh_k1",
        "agravity_qed_gamma_gamma_unpolarized_sqamp_tree",
        "bjorken_effective_charge_alpha_g1",
        "u1_2d_yang_mills_wilson_loop_area_response",
        "lqa_largeN_xi_in_log_mu",
        "lqa_largeN_xi_in_log_log_mu",
        "lqa_full_lambda_xi_trajectory_tensor_r_projection",
        "fqhe_nu_1_3_point_contact_conductance",
    } == targets


def test_every_entry_has_required_nonempty_fields_and_unique_target():
    entries = build_entries(REPO_ROOT)
    assert validate_entries(entries, REPO_ROOT) == []
    assert len({entry.target for entry in entries}) == len(entries)
    for entry in entries:
        record = entry.__dict__
        for field in REQUIRED_FIELDS:
            assert record[field] not in (None, "", [])


def test_every_source_candidate_has_registered_primary_evidence():
    entries = build_entries(REPO_ROOT)
    for entry in entries:
        if entry.target_type != "source_candidate":
            continue
        assert any(
            SOURCE_REGISTRY[source_id]["kind"] == "external_primary"
            for source_id in entry.evidence_source
        )
    for source in SOURCE_REGISTRY.values():
        if source["kind"] == "external_primary":
            assert source["url"].startswith("https://")
            assert "search" not in source["url"].lower()


def test_not_decidable_metric_remains_null_not_zero():
    entry = next(
        entry
        for entry in build_entries(REPO_ROOT)
        if entry.target == "agravity_qed_gamma_gamma_unpolarized_sqamp_tree"
    )

    assert entry.dprime_outcome == "not_decidable"
    assert entry.metric["value"] is None
    assert "degenerate" in entry.metric["reason"]


def test_model_fails_and_reparametrization_pass_never_become_claim_passes():
    ledger = build_ledger(REPO_ROOT)
    assert ledger["summary"]["physical_claim_pass_count"] == 0
    assert ledger["summary"]["physical_dprime_closed"] is False
    assert all(entry["claim_pass"] is False for entry in ledger["entries"])

    by_target = {entry["target"]: entry for entry in ledger["entries"]}
    assert by_target["bjorken_effective_charge_alpha_g1"]["dprime_outcome"] == "fail_model_bound"
    assert by_target["lqa_largeN_xi_in_log_log_mu"]["dprime_outcome"] == "pass_reparametrization_not_physical"


def test_current_result_artifacts_are_synchronized_into_ledger():
    ledger = build_ledger(REPO_ROOT)
    by_target = {entry["target"]: entry for entry in ledger["entries"]}
    ym_source = json.loads(
        (REPO_ROOT / "results/paper5/DPRIME_2D_YM_HEAT_KERNEL_GATE_2026-08-26.json").read_text(encoding="utf-8")
    )
    lqa_source = json.loads(
        (REPO_ROOT / "results/paper5/DPRIME_LQA_2D_TRAJECTORY_RPROJ_GATE_2026-08-26.json").read_text(encoding="utf-8")
    )
    transport_source = json.loads(
        (REPO_ROOT / "results/paper5/DPRIME_EXTERNAL_IR_SAFE_COMPOSITION_GATE_2026-08-26.json").read_text(encoding="utf-8")
    )

    assert by_target["u1_2d_yang_mills_wilson_loop_area_response"]["status"] == ym_source["status"]
    assert by_target["lqa_full_lambda_xi_trajectory_tensor_r_projection"]["status"] == lqa_source["status"]
    assert by_target["lqa_full_lambda_xi_trajectory_tensor_r_projection"]["metric"]["max_full_beta_residual"] == lqa_source["maxima"]["full_vector_residual"]
    assert by_target["fqhe_nu_1_3_point_contact_conductance"]["status"] == transport_source["status"]
    assert by_target["fqhe_nu_1_3_point_contact_conductance"]["metric"]["absolute_gap"] == transport_source["dprime_endpoint_gate"]["absolute_gap"]


def test_artifacts_are_deterministic_and_csv_preserves_required_columns(tmp_path):
    first = write_artifacts(tmp_path / "first", REPO_ROOT)
    second = write_artifacts(tmp_path / "second", REPO_ROOT)

    assert [path.name for path in first] == [
        SCHEMA_FILENAME,
        f"{ARTIFACT_STEM}.json",
        f"{ARTIFACT_STEM}.csv",
        f"{ARTIFACT_STEM}.md",
    ]
    for left, right in zip(first, second):
        assert left.read_bytes() == right.read_bytes()

    with first[2].open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames[: len(REQUIRED_FIELDS)] == list(REQUIRED_FIELDS)
        rows = list(reader)
    assert len(rows) == 14
    assert json.loads(rows[0]["evidence_source"])
    assert json.loads(rows[0]["preregistered_controls"])


def test_cli_writes_schema_and_three_ledger_formats(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "entries=14" in completed.stdout
    assert "physical_claim_passes=0" in completed.stdout
    assert len(list(tmp_path.iterdir())) == 4

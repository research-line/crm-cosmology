import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.dprime_external_ir_safe_composition_gate import (
    STATUS,
    build_report,
    projective_endpoint_limits,
    serial_transmission_probability,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "dprime_external_ir_safe_composition_gate.py"
RESULT = REPO_ROOT / "results" / "paper5" / "DPRIME_EXTERNAL_IR_SAFE_COMPOSITION_GATE_2026-08-26.json"
NOTE = REPO_ROOT / "research" / "crm-v" / "CRM5_DPRIME_EXTERNAL_IR_SAFE_COMPOSITION_SEARCH_V1_2026-08-26.md"
MANUSCRIPTS = (
    REPO_ROOT / "papers" / "extensions" / "Paper5_EN.tex",
    REPO_ROOT / "papers" / "extensions" / "Paper5_DE.tex",
)


def test_status_keeps_physical_dprime_open():
    report = build_report()

    assert report["status"] == STATUS
    assert report["summary"]["complete_candidate_count"] == 0
    assert report["summary"]["physical_dprime_closed"] is False
    assert report["summary"]["claim_upgrade_count"] == 0
    assert any("No physical D-prime derivation" in line for line in report["claim_boundary"])


def test_source_endpoint_powers_fail_constant_projective_generator():
    lower, upper = projective_endpoint_limits()
    gate = build_report()["dprime_endpoint_gate"]

    assert lower == pytest.approx(2.0)
    assert upper == pytest.approx(2.0 / 3.0)
    assert gate["absolute_gap"] == pytest.approx(4.0 / 3.0)
    assert gate["dprime_pass"] is False


def test_equal_scalar_inputs_do_not_close_under_exact_scattering_composition():
    zero = serial_transmission_probability(0.0)
    half_pi = serial_transmission_probability(math.pi / 2.0)
    counterexample = build_report()["scalar_composition_counterexample"]

    assert zero == pytest.approx(1.0 / 9.0)
    assert half_pi == pytest.approx(1.0)
    assert counterexample["individual_transmission_probabilities"] == [0.5, 0.5]
    assert counterexample["same_scalar_inputs_different_output"] is True


def test_near_candidate_has_physical_boundaries_but_no_scalar_composition():
    candidate = build_report()["primary_near_candidate"]

    assert candidate["boundary_responses"]["finite_and_distinguishable"] is True
    assert candidate["criteria"]["physical_transport_observable"] == "SUPPORTED"
    assert candidate["criteria"]["IR_finite_endpoints"] == "SUPPORTED_IN_THE_NU_1_3_TRANSPORT_MODEL"
    assert candidate["criteria"]["exact_binary_scalar_conductance_composition"] == "NOT_SOURCE_DEFINED"
    assert "TBA-weighted" in candidate["composition_boundary"]["physical_observable_construction"]


def test_source_registry_contains_direct_primary_sources():
    sources = build_report()["source_registry"]

    assert len(sources) == 5
    assert all(source["kind"] == "external_primary" for source in sources.values())
    for source in sources.values():
        assert source["url"].startswith("https://")
        assert "search" not in source["url"].lower()


def test_cli_output_matches_committed_result(tmp_path):
    output = tmp_path / "transport.json"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert STATUS in completed.stdout
    assert output.read_bytes() == RESULT.read_bytes()
    assert json.loads(output.read_text(encoding="utf-8")) == build_report()


def test_research_note_and_bilingual_manuscripts_freeze_claim_boundary():
    note = NOTE.read_text(encoding="utf-8")
    assert STATUS in note
    assert "2/3" in note
    assert "1/9" in note

    for manuscript in MANUSCRIPTS:
        text = manuscript.read_text(encoding="utf-8")
        assert "FendleyLudwigSaleur1995" in text
        assert "GhoshalZamolodchikov1994" in text
        assert "KostrykinSchrader2001" in text
        assert r"\frac{2}{3}" in text


def test_ledger_entry_is_synchronized_with_transport_result():
    from scripts.paper5.build_dprime_evidence_ledger import build_entries

    report = build_report()
    entry = next(
        row
        for row in build_entries(REPO_ROOT)
        if row.target == "fqhe_nu_1_3_point_contact_conductance"
    )

    assert entry.status == report["status"]
    assert entry.metric["lower_limit"] == report["dprime_endpoint_gate"]["lower_limit"]
    assert entry.metric["upper_limit"] == report["dprime_endpoint_gate"]["upper_limit"]
    assert entry.claim_pass is False

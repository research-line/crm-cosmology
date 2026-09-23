import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.dprime_massless_rg_scattering_gate import (
    STATUS,
    build_report,
    induced_rapidity_composition,
    marked_projective_ratio,
    massless_rl_amplitude,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "dprime_massless_rg_scattering_gate.py"
RESULT = REPO_ROOT / "results" / "paper5" / "DPRIME_MASSLESS_RG_SCATTERING_GATE_2026-08-26.json"
NOTE = REPO_ROOT / "research" / "crm-v" / "CRM5_DPRIME_IR_SAFE_EXACT_COMPOSITION_SOURCE_SEARCH_V2_2026-08-26.md"
MANUSCRIPTS = (
    REPO_ROOT / "papers" / "extensions" / "Paper5_EN.tex",
    REPO_ROOT / "papers" / "extensions" / "Paper5_DE.tex",
)


def test_exact_amplitude_has_unit_modulus_and_finite_distinct_boundaries():
    for theta in (-8.0, -1.0, 0.0, 2.0, 9.0):
        assert abs(massless_rl_amplitude(theta)) == pytest.approx(1.0, abs=1e-14)

    assert massless_rl_amplitude(-40.0) == pytest.approx(1.0 + 0.0j, abs=1e-14)
    assert massless_rl_amplitude(40.0) == pytest.approx(-1.0 + 0.0j, abs=1e-14)


def test_marked_projective_ratio_is_exactly_exp_theta():
    for theta in (-9.0, -2.5, 0.0, 1.25, 7.0):
        ratio = marked_projective_ratio(massless_rl_amplitude(theta))
        assert ratio == pytest.approx(complex(math.exp(theta)), rel=2e-12, abs=1e-13)


def test_induced_rapidity_law_has_audit_identity_and_zero_defect():
    identity = massless_rl_amplitude(0.0)
    left = massless_rl_amplitude(-0.8)
    right = massless_rl_amplitude(2.1)

    assert identity == pytest.approx(1j, abs=1e-14)
    assert induced_rapidity_composition(left, identity) == pytest.approx(left, abs=1e-14)
    assert induced_rapidity_composition(left, right) == pytest.approx(
        massless_rl_amplitude(1.3), abs=1e-14
    )


def test_physical_factorization_is_not_relabelled_as_response_composition():
    report = build_report()
    gate = report["physical_composition_gate"]
    candidate = report["candidate"]

    assert "S12" in gate["source_law"]
    assert gate["pass"] is False
    assert candidate["criteria"]["exact_binary_response_composition"] == "NOT_SOURCE_DEFINED"
    assert candidate["criteria"]["source_defined_neutral_identity_response"].startswith(
        "NOT_SUPPORTED"
    )


def test_running_coupling_and_real_response_transfers_remain_open():
    report = build_report()
    criteria = report["candidate"]["criteria"]

    assert criteria["source_defined_RG_crossover"] == "SUPPORTED_BY_TBA_C_FUNCTION"
    assert criteria["running_scalar_coupling_identified_with_response"] == "NOT_SOURCE_DEFINED"
    assert criteria["real_Paper_V_response_interval"].startswith("NOT_SUPPORTED")
    assert report["summary"]["complete_physical_candidate_count"] == 0


def test_status_keeps_physical_dprime_open_without_claim_upgrade():
    report = build_report()

    assert report["status"] == STATUS
    assert report["marked_projective_audit"]["algebraic_projective_identity_pass"] is True
    assert report["marked_projective_audit"]["physical_Dprime_pass"] is False
    assert report["summary"]["physical_dprime_closed"] is False
    assert report["summary"]["claim_upgrade_count"] == 0


def _assert_nested_approx_equal(actual, expected, abs_tol=1e-12, rel_tol=1e-9):
    if isinstance(actual, dict) and isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for k in actual:
            _assert_nested_approx_equal(actual[k], expected[k], abs_tol=abs_tol, rel_tol=rel_tol)
    elif isinstance(actual, list) and isinstance(expected, list):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected, strict=True):
            _assert_nested_approx_equal(a, e, abs_tol=abs_tol, rel_tol=rel_tol)
    elif isinstance(actual, float) and isinstance(expected, float):
        assert math.isclose(actual, expected, abs_tol=abs_tol, rel_tol=rel_tol)
    else:
        assert actual == expected


def test_cli_output_matches_committed_result(tmp_path):
    output = tmp_path / "massless-flow.json"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert STATUS in completed.stdout
    _assert_nested_approx_equal(
        json.loads(output.read_text(encoding="utf-8")),
        json.loads(RESULT.read_text(encoding="utf-8")),
    )
    assert json.loads(output.read_text(encoding="utf-8")) == build_report()


def test_note_readme_and_bilingual_manuscripts_freeze_the_category_boundary():
    note = NOTE.read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert STATUS in note
    assert "S_RL(theta_1 + theta_2)" in note
    assert NOTE.name in readme
    for manuscript in MANUSCRIPTS:
        text = manuscript.read_text(encoding="utf-8")
        assert "FendleySaleurZamolodchikov1993" in text
        assert r"S_{RL}(\theta)&=-\tanh" in text
        assert "Yang--Baxter" in text

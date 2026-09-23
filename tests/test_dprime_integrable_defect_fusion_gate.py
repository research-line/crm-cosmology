import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.dprime_integrable_defect_fusion_gate import (
    STATUS,
    build_report,
    dprime_defect,
    fuse_defect_couplings,
    fuse_normalized_couplings,
    fused_amplitudes,
    ising_defect_angle,
    marked_projective_ratio,
    reflection_amplitude,
    reflection_probability,
    transmission_amplitude,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "dprime_integrable_defect_fusion_gate.py"
RESULT = (
    REPO_ROOT
    / "results"
    / "paper5"
    / "DPRIME_INTEGRABLE_DEFECT_FUSION_GATE_2026-08-26.json"
)
NOTE = (
    REPO_ROOT
    / "research"
    / "crm-v"
    / "CRM5_DPRIME_INTEGRABLE_DEFECT_FUSION_SOURCE_SEARCH_V1_2026-08-26.md"
)
MANUSCRIPTS = (
    REPO_ROOT / "papers" / "extensions" / "Paper5_EN.tex",
    REPO_ROOT / "papers" / "extensions" / "Paper5_DE.tex",
)


def test_source_branch_has_transparent_neutral_and_reflective_endpoint():
    theta = 0.8

    assert ising_defect_angle(0.0) == 0.0
    assert ising_defect_angle(2.0) == pytest.approx(-math.pi / 2.0)
    assert transmission_amplitude(theta, 0.0) == 1.0 + 0.0j
    assert reflection_amplitude(theta, 0.0) == 0.0 + 0.0j
    assert abs(transmission_amplitude(theta, 2.0)) == pytest.approx(0.0, abs=1e-15)
    assert abs(reflection_amplitude(theta, 2.0)) == pytest.approx(1.0, abs=1e-14)

    with pytest.raises(ValueError):
        ising_defect_angle(-0.1)


def test_exact_coupling_fusion_has_identity_associativity_and_upper_absorber():
    for coupling in (0.0, 0.4, 1.1, 2.0):
        assert fuse_defect_couplings(coupling, 0.0) == pytest.approx(coupling)

    left, middle, right = 0.3, 0.8, 1.2
    assert fuse_defect_couplings(fuse_defect_couplings(left, middle), right) == pytest.approx(
        fuse_defect_couplings(left, fuse_defect_couplings(middle, right))
    )
    assert fuse_defect_couplings(2.0, 0.7) == pytest.approx(2.0)


def test_marked_projective_quotient_multiplies_exactly_on_positive_semigroup():
    for left, right in ((0.1, 0.2), (0.35, 0.4), (0.7, 0.15)):
        fused = fuse_normalized_couplings(left, right)
        assert marked_projective_ratio(fused) == pytest.approx(
            marked_projective_ratio(left) * marked_projective_ratio(right),
            abs=2e-14,
        )
        assert dprime_defect(left, right) == pytest.approx(0.0, abs=2e-15)


def test_multiple_scattering_fusion_closes_on_single_defect_family():
    for theta, left, right in ((-1.2, 0.4, 0.8), (0.7, 1.0, 0.6), (2.1, 1.4, 0.3)):
        fused_coupling = fuse_defect_couplings(left, right)
        fused_transmission, fused_reflection = fused_amplitudes(theta, left, right)
        assert fused_transmission == pytest.approx(
            transmission_amplitude(theta, fused_coupling), abs=2e-14
        )
        assert fused_reflection == pytest.approx(
            reflection_amplitude(theta, fused_coupling), abs=2e-14
        )


def test_scalar_reflection_probability_does_not_supply_signed_interior_identity():
    theta = 0.7
    left, right = 0.8, 0.6
    fused = fuse_defect_couplings(left, right)

    assert reflection_probability(theta, 0.0) == 0.0
    assert reflection_probability(theta, 2.0) == pytest.approx(1.0, abs=1e-14)
    assert 0.0 < reflection_probability(theta, left) < 1.0
    assert 0.0 < reflection_probability(theta, right) < 1.0
    assert 0.0 < reflection_probability(theta, fused) < 1.0

    report = build_report()
    control = report["scalar_observable_transfer_control"]
    assert "endpoint" in control["neutral_location"]
    assert abs(control["Dprime_defect"]) > 1.0
    assert control["quotient_fused"] != pytest.approx(control["quotient_product"])
    assert control["projective_law_inherited"] is False


def test_RG_and_signed_response_gates_keep_physical_Dprime_open():
    report = build_report()
    criteria = report["candidate"]["criteria"]

    assert criteria["source_defined_exact_binary_physical_fusion"] == "SUPPORTED"
    assert criteria["projective_quotient_on_normalized_coupling"] == (
        "EXACT_ON_POSITIVE_SEMIGROUP"
    )
    assert criteria["two_sided_signed_response_interval"] == "NOT_SOURCE_AUDITED"
    assert criteria["coupling_is_running_scalar_response"] == "NOT_SOURCE_DEFINED"
    assert criteria["fusion_is_RG_semigroup"] == "EXPLICITLY_LEFT_OPEN_BY_SOURCE"
    assert report["RG_transfer_gate"]["pass"] is False
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
    output = tmp_path / "defect-fusion.json"
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


def test_note_readme_and_bilingual_manuscripts_freeze_the_RG_category_boundary():
    note = NOTE.read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert STATUS in note
    assert "ma -> 0" in note
    assert "g_I(mu)" in note
    assert NOTE.name in readme
    for manuscript in MANUSCRIPTS:
        text = manuscript.read_text(encoding="utf-8")
        assert "HeJiangLiu2026" in text
        assert r"g_{I,f}" in text
        assert "2605.20688v1" in text

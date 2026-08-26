import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.smooth_collar_classification_gate import (
    AUDIT_PROFILES,
    PROJECTIVE,
    STATUS,
    build_report,
    canonical_generator,
    canonical_kappa,
    collar_inverse,
    collar_q,
    collar_q_derivative,
    compose,
    fixed_projective_defect,
    gauge_coboundary,
    gauge_map_to_projective,
    linear_profile,
    projective_compose,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts/paper5/smooth_collar_classification_gate.py"
RESULT = REPO_ROOT / "results/paper5/SMOOTH_COLLAR_CLASSIFICATION_GATE_2026-08-26.json"
NOTE = REPO_ROOT / "research/crm-v/CRM5_SMOOTH_COLLAR_OPERATIONS_CLASSIFICATION_V1_2026-08-26.md"
MANUSCRIPTS = (
    REPO_ROOT / "papers/extensions/Paper5_EN.tex",
    REPO_ROOT / "papers/extensions/Paper5_DE.tex",
)


def test_canonical_q_is_a_boundary_defining_diffeomorphism():
    for profile in AUDIT_PROFILES:
        assert collar_q(0.0, profile) == pytest.approx(1.0)
        assert collar_q(1.0, profile) == pytest.approx(0.0)
        assert collar_q_derivative(0.0, profile) < 0.0
        assert collar_q_derivative(1.0, profile) < 0.0
        for index in range(2001):
            assert collar_q_derivative(index / 2000.0, profile) < 0.0


def test_q_inverse_and_composition_have_exact_boundary_contract():
    profile = linear_profile(0.25)
    for x in (0.0, 0.1, 0.4, 0.8, 0.97, 1.0):
        assert collar_inverse(collar_q(x, profile), profile) == pytest.approx(x)
        assert compose(x, 0.0, profile) == pytest.approx(x)
        assert compose(x, 1.0, profile) == pytest.approx(1.0)


def test_pullback_of_multiplication_is_commutative_and_associative():
    for profile in AUDIT_PROFILES:
        for x, y, z in (
            (0.07, 0.22, 0.61),
            (0.18, 0.49, 0.83),
            (0.37, 0.58, 0.91),
        ):
            assert compose(x, y, profile) == pytest.approx(compose(y, x, profile))
            assert compose(compose(x, y, profile), z, profile) == pytest.approx(
                compose(x, compose(y, z, profile), profile), abs=2e-13
            )
            combined = compose(x, y, profile)
            assert collar_q(combined, profile) == pytest.approx(
                collar_q(x, profile) * collar_q(y, profile), abs=2e-13
            )


def test_linear_family_has_frozen_generator_and_simple_boundary_zero():
    epsilon = 0.25
    profile = linear_profile(epsilon)
    for x in (0.0, 0.2, 0.7, 0.95, 1.0):
        expected = (1.0 + epsilon) * (1.0 - x * x) / (
            1.0 + epsilon * (1.0 - x * x)
        )
        assert canonical_generator(x, profile) == pytest.approx(expected)
    assert canonical_generator(0.0, profile) == pytest.approx(1.0)
    assert canonical_generator(1.0, profile) == pytest.approx(0.0)
    assert canonical_kappa(profile) == pytest.approx(2.5)
    delta = 1e-7
    boundary_derivative = (
        canonical_generator(1.0, profile)
        - canonical_generator(1.0 - delta, profile)
    ) / delta
    assert boundary_derivative == pytest.approx(-canonical_kappa(profile), rel=2e-7)


def test_h_gauge_is_exact_smooth_conjugacy_to_projective_addition():
    for profile in AUDIT_PROFILES:
        for x, y in ((0.12, 0.31), (0.45, 0.72), (0.78, 0.91)):
            left = gauge_map_to_projective(compose(x, y, profile), profile)
            right = projective_compose(
                gauge_map_to_projective(x, profile),
                gauge_map_to_projective(y, profile),
            )
            assert left == pytest.approx(right, abs=2e-13)


def test_fixed_projective_defect_is_the_exact_h_coboundary():
    x, y = 0.2, 0.35
    assert fixed_projective_defect(x, y, PROJECTIVE) == pytest.approx(0.0, abs=1e-13)
    for profile in AUDIT_PROFILES[1:]:
        defect = fixed_projective_defect(x, y, profile)
        assert defect == pytest.approx(gauge_coboundary(x, y, profile), abs=2e-13)
        assert abs(defect) > 1e-5


def test_odd_h_profiles_supply_the_signed_B_prime_germ():
    profile = linear_profile(0.25)
    for x in (0.05, 0.2, 0.6, 0.9):
        positive_generator = -math.log(collar_q(x, profile))
        negative_generator = -math.log(collar_q(-x, profile))
        assert negative_generator == pytest.approx(-positive_generator, abs=1e-14)


def test_report_limits_completeness_to_the_declared_strict_class():
    report = build_report()
    scope = report["classification_scope"]
    summary = report["summary"]

    assert report["status"] == STATUS
    assert summary["complete_within_declared_smooth_strict_class"] is True
    assert summary["infinite_dimensional_h_gauge_exposed"] is True
    assert summary["physical_UV_selection_derived"] is False
    assert summary["claim_upgrade_count"] == 0
    assert "nilpotent or noncancellative t-conorms" in scope["excluded"]
    assert "multi-channel or stochastic response laws" in scope["excluded"]
    assert report["classification_theorem"]["projective_slice"] == (
        "D-prime holds if and only if h=0"
    )
    for audit in report["profile_audits"]:
        assert max(audit["maximum_residuals"].values()) < 2e-12


def test_cli_output_and_json_are_deterministic(tmp_path):
    output = tmp_path / "collars.json"
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


def test_note_and_bilingual_manuscripts_freeze_scope_and_classification():
    note = NOTE.read_text(encoding="utf-8")
    assert STATUS in note
    assert "q_h(x)" in note
    assert "D-prime holds exactly at h=0" in note

    for manuscript in MANUSCRIPTS:
        text = manuscript.read_text(encoding="utf-8")
        assert text.count(r"\label{prop:smooth_collar_classification}") == 1
        assert r"q_h(x)" in text
        assert r"H_h&=q_0^{-1}\circ q_h" in text
        assert "SMOOTH_COLLAR_CLASSIFICATION_GATE_2026-08-26.json" in text

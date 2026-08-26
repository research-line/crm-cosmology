import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.paper5.axiom_c_bump_separation_gate import (
    EPSILON,
    STATUS,
    WITNESS_G,
    build_report,
    compact_bump,
    compact_bump_derivative,
    headroom_certificate,
    odd_bump,
    response,
    response_derivative,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "paper5" / "axiom_c_bump_separation_gate.py"
RESULT = REPO_ROOT / "results" / "paper5" / "AXIOM_C_BUMP_SEPARATION_GATE_2026-08-26.json"
NOTE = REPO_ROOT / "research" / "crm-v" / "CRM5_DPRIME_TANH_EPSILON_BUMP_C_INDEPENDENCE_SEPARATION_V1_2026-08-26.md"
MANUSCRIPTS = (
    REPO_ROOT / "papers" / "extensions" / "Paper5_EN.tex",
    REPO_ROOT / "papers" / "extensions" / "Paper5_DE.tex",
)


def test_standard_bump_has_frozen_support_and_zero_extension():
    assert compact_bump(0.0) == pytest.approx(1.0)
    for z in (-2.0, -1.0, 1.0, 2.0):
        assert compact_bump(z) == 0.0
        assert compact_bump_derivative(z) == 0.0
    assert compact_bump(0.5) == pytest.approx(math.exp(-1.0 / 3.0))


def test_translated_bump_and_response_are_odd():
    for g in (-4.0, -2.2, -2.0, -1.8, -0.5, 0.0, 0.5, 1.8, 2.0, 2.2, 4.0):
        assert odd_bump(-g) == pytest.approx(-odd_bump(g), abs=1e-15)
        assert response(-g) == pytest.approx(-response(g), abs=1e-15)


def test_local_series_is_exactly_tanh_near_origin():
    for g in (-1.75, -1.0, -0.1, 0.0, 0.1, 1.0, 1.75):
        assert response(g) == pytest.approx(math.tanh(g), abs=1e-15)
    assert response_derivative(0.0) == pytest.approx(1.0)


def test_positive_branch_capacity_has_analytic_headroom():
    certificate = headroom_certificate()
    assert certificate["maximum_bump_to_headroom_ratio"] == pytest.approx(0.5887518864565877)
    assert certificate["strictly_below_one"] is True

    for index in range(20001):
        g = 4.0 * index / 20000.0
        assert 0.0 <= response(g) < 1.0


def test_explicit_witness_violates_monotonicity_but_keeps_endpoint_limit():
    expected = 1.0 / math.cosh(WITNESS_G) ** 2 - (32.0 / 225.0) * math.exp(-1.0 / 3.0)
    report = build_report()
    certificate = report["monotonicity_certificate"]

    assert EPSILON == pytest.approx(1.0 / 50.0)
    assert response_derivative(WITNESS_G) == pytest.approx(expected)
    assert expected < 0.0
    assert certificate["negative_at_witness"] is True
    assert certificate["endpoint_saturation_retained"] is True
    assert response(30.0) == pytest.approx(1.0)


def test_ledger_limits_the_independence_claim_to_the_proved_scope():
    report = build_report()
    ledger = report["axiom_ledger"]

    assert report["status"] == STATUS
    assert ledger["A_finite_positive_branch_capacity"].startswith("PASS")
    assert ledger["B_local_odd_expansion_positive_slope"].startswith("PASS")
    assert ledger["B_prime_global_odd_extension"].startswith("PASS")
    assert ledger["C_monotone_control"].startswith("FAIL")
    assert ledger["D_response_composition"] == "NOT_CLAIMED"
    assert ledger["D_plus_minus_global_group_homomorphism"].startswith("INCOMPATIBLE")
    assert report["summary"]["does_not_separate_C_from"] == ["global_D_plus_minus_homomorphism"]


def test_cli_output_is_deterministic(tmp_path):
    output = tmp_path / "bump.json"
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


def test_note_and_bilingual_manuscripts_freeze_verified_witness_and_guardrail():
    note = NOTE.read_text(encoding="utf-8")
    assert STATUS in note
    assert "17/8" in note
    assert "0.588751886" in note
    assert "D^pm" in note

    for manuscript in MANUSCRIPTS:
        text = manuscript.read_text(encoding="utf-8")
        assert "b(4(g-2))" in text
        assert r"\frac{17}{8}" in text
        assert r"\frac{32}{225}" in text
        assert "AXIOM_C_BUMP_SEPARATION_GATE_2026-08-26.json" in text

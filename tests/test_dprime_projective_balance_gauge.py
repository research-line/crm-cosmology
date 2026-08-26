import json
import math
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPO_ROOT / "results/paper5/DPRIME_PROJECTIVE_BALANCE_GAUGE_AUDIT_2026-08-26.json"
EN_PATH = REPO_ROOT / "papers/extensions/Paper5_EN.tex"
DE_PATH = REPO_ROOT / "papers/extensions/Paper5_DE.tex"


def _ledger():
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _normalized_boundary_odds(lower, upper, neutral, value):
    return ((value - lower) / (upper - value)) / (
        (neutral - lower) / (upper - neutral)
    )


def _mobius(value, a, b, c, d):
    return (a * value + b) / (c * value + d)


def _inverse_phi(value, epsilon):
    lower = -1.0 + 1e-12
    upper = 1.0 - 1e-12
    for _ in range(100):
        middle = (lower + upper) / 2.0
        if math.atanh(middle) + epsilon * middle < value:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2.0


def test_audit_result_refuses_physical_claim_upgrade():
    ledger = _ledger()

    assert ledger["result"] == (
        "CONDITIONAL_PROJECTIVE_CANONICALITY__PHYSICAL_SELECTION_OPEN__NO_CLAIM_UPGRADE"
    )
    assert ledger["summary"]["physical_selection_derived"] is False
    assert ledger["summary"]["D_prime_remains_explicit_assumption"] is True
    assert ledger["summary"]["claim_upgrade_count"] == 0


def test_projective_quotient_is_normalized_boundary_cross_ratio():
    for x in (-0.8, -0.25, 0.0, 0.4, 0.9):
        quotient = (1.0 + x) / (1.0 - x)
        cross_ratio = _normalized_boundary_odds(-1.0, 1.0, 0.0, x)

        assert math.isclose(quotient, cross_ratio, rel_tol=1e-14)
        assert math.isclose(0.5 * math.log(quotient), math.atanh(x), rel_tol=1e-14)


def test_normalized_cross_ratio_is_invariant_under_projective_chart_change():
    coefficients = (1.2, 0.1, 0.2, 1.1)
    lower, upper, neutral = -1.0, 1.0, 0.0
    transformed_marks = [
        _mobius(point, *coefficients) for point in (lower, upper, neutral)
    ]

    for x in (-0.75, -0.1, 0.3, 0.85):
        original = _normalized_boundary_odds(lower, upper, neutral, x)
        transformed = _normalized_boundary_odds(
            *transformed_marks, _mobius(x, *coefficients)
        )

        assert math.isclose(original, transformed, rel_tol=1e-13)


def test_neutral_mark_removes_boundary_preserving_projective_scale():
    def boundary_stabilizer(x, k):
        return ((k - 1.0) + (k + 1.0) * x) / (
            (k + 1.0) + (k - 1.0) * x
        )

    for k in (0.25, 0.75, 2.0, 4.0):
        assert math.isclose(boundary_stabilizer(-1.0, k), -1.0)
        assert math.isclose(boundary_stabilizer(1.0, k), 1.0)
        assert not math.isclose(boundary_stabilizer(0.0, k), 0.0)
        for x in (-0.5, 0.2, 0.7):
            transformed = boundary_stabilizer(x, k)
            assert math.isclose(
                (1.0 + transformed) / (1.0 - transformed),
                k * (1.0 + x) / (1.0 - x),
                rel_tol=1e-13,
            )

    assert boundary_stabilizer(0.0, 1.0) == 0.0


def test_nonprojective_collar_has_its_own_balance_but_fails_fixed_R():
    epsilon = 0.25
    x, y = 0.2, 0.35
    phi_x = math.atanh(x) + epsilon * x
    phi_y = math.atanh(y) + epsilon * y
    composed = _inverse_phi(phi_x + phi_y, epsilon)

    def R(value):
        return (1.0 + value) / (1.0 - value)

    def Q(value):
        return R(value) * math.exp(2.0 * epsilon * value)

    assert math.isclose(Q(composed), Q(x) * Q(y), rel_tol=1e-12)
    fixed_R_defect = math.log(R(composed)) - math.log(R(x)) - math.log(R(y))
    analytic_defect = -2.0 * epsilon * (composed - x - y)
    assert math.isclose(fixed_R_defect, analytic_defect, abs_tol=1e-12)
    assert abs(fixed_R_defect) > 1e-4


def test_bilingual_manuscripts_state_marked_projective_contract():
    en = EN_PATH.read_text(encoding="utf-8")
    de = DE_PATH.read_text(encoding="utf-8")

    for marker in (
        r"\frac{(x-b_-)/(b_+-x)}{(e-b_-)/(b_+-e)}",
        r"Q_\varepsilon(x):=e^{2\phi_\varepsilon(x)}",
        r"\cite{PapadopoulosTroyanov2008,RainioVuorinen2023}",
    ):
        assert en.count(marker) == 1
        assert de.count(marker) == 1
    assert "Marked-projective naturality audit" in en
    assert "Markiert-projektives Natürlichkeitsaudit" in de


def test_manuscripts_correct_multiplicative_additive_category():
    en = EN_PATH.read_text(encoding="utf-8")
    de = DE_PATH.read_text(encoding="utf-8")

    assert "rather than the ratio itself, is additive" in en
    assert "nicht der Quotient selbst" in de
    assert "the ratio of distances to the two saturation faces is the additive" not in en
    assert "das Verhältnis der Abstände zu den beiden Sättigungsflächen die additive" not in de


def test_physical_gate_requires_observable_marking_and_exact_composition():
    gate = _ledger()["physical_selection_gate"]

    assert gate["current_status"] == "OPEN_NO_SOURCE_DERIVATION"
    assert set(gate["requirements"]) == {
        "source-defined gauge-invariant observable",
        "two finite distinguishable predeclared boundary responses",
        "source-defined neutral identity response",
        "exact independently sourced binary response composition",
        "evidence that signed Hilbert increments of the marked observable add",
    }

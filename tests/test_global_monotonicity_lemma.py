import json
import math
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPO_ROOT / "results/paper5/MONOTONICITY_LEMMA_GLOBAL_GROUP_2026-08-26.json"
EN_PATH = REPO_ROOT / "papers/extensions/Paper5_EN.tex"
DE_PATH = REPO_ROOT / "papers/extensions/Paper5_DE.tex"


def _ledger():
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _inverse_phi(value, epsilon):
    lower = -1.0 + 1e-12
    upper = 1.0 - 1e-12
    for _ in range(100):
        middle = (lower + upper) / 2.0
        phi_middle = math.atanh(middle) + epsilon * middle
        if phi_middle < value:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2.0


def test_ledger_declares_exact_global_hypotheses():
    ledger = _ledger()
    hypothesis_ids = {item["id"] for item in ledger["hypotheses"]}

    assert hypothesis_ids == {
        "H1_GLOBAL_RESPONSE_GROUP",
        "H2_TRANSLATION_DIFFEOMORPHISMS",
        "H3_GLOBAL_CONTROL_HOMOMORPHISM",
        "H4_POSITIVE_ORIENTATION",
    }
    assert ledger["claim"]["control_group"] == "(R,+)"


def test_proof_ledger_excludes_circular_or_projective_inputs():
    boundary = _ledger()["dependency_boundary"]

    assert set(boundary["does_not_use"]) == {
        "prior_monotonicity_of_sigma",
        "Axiom_C",
        "Abel_coordinate_phi",
        "projective_assumption_D_prime",
    }
    assert "local_additive_chart_only" in boundary["not_implied_by"]
    assert "positive_local_slope_only" in boundary["not_implied_by"]


def test_normalization_audit_distinguishes_scaled_and_unscaled_slopes():
    audit = _ledger()["normalization_audit"]

    assert audit["axiom_B_unscaled_slope"] == "dS_T/dg(0)=c_1>0"
    assert audit["normalized_slope"] == "dsigma/dg(0)=c_1/S_max>0"
    assert audit["rejected_identity"] == "sigma_prime(0)=c_1"


def test_bilingual_manuscripts_contain_the_same_global_lemma_contract():
    en = EN_PATH.read_text(encoding="utf-8")
    de = DE_PATH.read_text(encoding="utf-8")

    for marker in (
        r"\label{lem:global_monotonicity}",
        r"\label{eq:global_monotonicity_generator}",
    ):
        assert en.count(marker) == 1
        assert de.count(marker) == 1
    for marker in (r"\sigma:(\mathbb{R},+)", r"c_1/S_{\max}"):
        assert en.count(marker) == de.count(marker)
        assert en.count(marker) >= 1
    assert "No monotonicity of $\\sigma$" in en
    assert "weder eine Monotonie von $\\sigma$" in de


def test_local_positive_slope_does_not_force_global_monotonicity():
    def derivative(u):
        phase = u + 2.0 * math.sin(u)
        return (1.0 / math.cosh(phase) ** 2) * (1.0 + 2.0 * math.cos(u))

    assert derivative(0.0) == 3.0
    assert derivative(math.pi) < 0.0


def test_projective_positive_control_satisfies_generator_identity():
    kappa = 1.7
    for u in (-3.0, -0.5, 0.0, 0.75, 2.5):
        sigma = math.tanh(kappa * u)
        generator = 1.0 - sigma**2
        analytic_derivative = kappa / math.cosh(kappa * u) ** 2

        assert generator > 0.0
        assert math.isclose(analytic_derivative, kappa * generator, rel_tol=1e-12)


def test_nonprojective_collar_is_monotone_without_satisfying_d_prime():
    epsilon = 0.3
    x = 0.2
    y = 0.35
    phi_sum = math.atanh(x) + epsilon * x + math.atanh(y) + epsilon * y
    composed = _inverse_phi(phi_sum, epsilon)
    d_prime_defect = math.atanh(composed) - math.atanh(x) - math.atanh(y)

    for sample in (-0.9, -0.2, 0.0, 0.4, 0.95):
        generator = (1.0 - sample**2) / (1.0 + epsilon * (1.0 - sample**2))
        assert generator > 0.0
    assert abs(d_prime_defect) > 1e-4


def test_summary_refuses_unconditional_axiom_c_redundancy():
    summary = _ledger()["summary"]

    assert summary["global_monotonicity_secured"] is True
    assert summary["prior_profile_monotonicity_used"] is False
    assert summary["D_prime_used"] is False
    assert summary["axiom_C_unconditionally_redundant"] is False
    assert summary["claim_upgrade_count"] == 0

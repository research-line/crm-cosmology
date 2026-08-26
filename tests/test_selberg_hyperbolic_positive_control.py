import json
import math
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = REPO_ROOT / "results/paper5/SELBERG_HYPERBOLIC_POSITIVE_CONTROL_2026-08-26.json"
EN_PATH = REPO_ROOT / "papers/extensions/Paper5_EN.tex"
DE_PATH = REPO_ROOT / "papers/extensions/Paper5_DE.tex"


def _ledger():
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _multiply(left, right):
    return [
        [
            sum(left[row][index] * right[index][column] for index in range(2))
            for column in range(2)
        ]
        for row in range(2)
    ]


def _boost(rapidity):
    return [
        [math.cosh(rapidity), math.sinh(rapidity)],
        [math.sinh(rapidity), math.cosh(rapidity)],
    ]


def test_audit_result_limits_positive_control_and_refuses_claim_upgrade():
    ledger = _ledger()

    assert ledger["result"] == (
        "HYPERBOLIC_LIE_MOTIF_PASS__FULL_E10_TRANSFER_REJECTED__NO_COSMOLOGY_OR_DPRIME_CLAIM"
    )
    assert ledger["positive_control_scope"]["status"] == "PASS_LIE_ORIGIN_COMMUTANT_ONLY"
    assert ledger["summary"]["claim_upgrade_count"] == 0


def test_collinear_boost_matrices_form_the_required_one_parameter_group():
    for u, v in ((-1.2, 0.4), (-0.25, -0.7), (0.0, 1.1), (0.8, 1.3)):
        product = _multiply(_boost(u), _boost(v))
        expected = _boost(u + v)

        for row in range(2):
            for column in range(2):
                assert math.isclose(
                    product[row][column], expected[row][column], rel_tol=1e-13, abs_tol=1e-13
                )


def test_boost_rapidity_gives_projective_crm_composition():
    for u, v in ((-0.9, 0.2), (0.1, 0.7), (0.8, 1.4)):
        x = math.tanh(u)
        y = math.tanh(v)
        composed = (x + y) / (1.0 + x * y)

        assert math.isclose(composed, math.tanh(u + v), rel_tol=1e-14, abs_tol=1e-14)
        assert -1.0 < composed < 1.0


def test_e10_audit_has_no_full_axiom_passes():
    rows = {row["id"]: row["status"] for row in _ledger()["e10_audit"]}

    assert rows == {
        "A_FINITE_RESPONSE_CAPACITY": "CATEGORY_MISMATCH_NOT_ESTABLISHED",
        "B_COOPERATIVE_REINFORCEMENT": "CATEGORY_MISMATCH_NOT_ESTABLISHED",
        "B_PRIME_RESPONSE_ODDNESS": "CATEGORY_MISMATCH_NOT_ESTABLISHED",
        "C_MONOTONE_COSMIC_CONTROL": "OUT_OF_SCOPE_NOT_ESTABLISHED",
        "D_RESPONSE_COMPOSITION": "SOURCE_SIDE_COMPOSITION_MOTIF_ONLY",
        "D_PM_REVERSIBLE_ONE_CHANNEL": "SUBGROUP_MOTIF_ONLY",
        "D_PRIME_PROJECTIVE_BOUNDARY_QUOTIENT": "NOT_ESTABLISHED",
    }
    assert _ledger()["summary"]["full_E10_satisfied"] is False


def test_historical_source_path_is_resolved_without_mutating_onedrive():
    audit = _ledger()["source_location_audit"]

    assert audit["stale_todo_path"] == ".LAB/.ZETA-ZOO/FST_MATHEMATICS/selberg/"
    assert audit["resolved_read_only_path"] == ".LAB/.ZETA-ZOO/CORE/selberg/"
    assert audit["source_lock_found"] is False
    assert audit["source_cloud_lock_risk"] == "HIGH_CLDFLT_SYS_READ_ONLY"


def test_rejected_equivalences_are_explicit_and_complete():
    rejected = set(_ledger()["rejected_equivalences"])

    assert rejected == {
        "C2_X_trivial if and only if E10_satisfied",
        "E10_satisfied if and only if saturation_embedding_exists",
        "shared_hyperbolic_motif implies same_geometry_or_same_physics",
    }


def test_bilingual_manuscripts_contain_same_selberg_guardrail_and_sources():
    en = EN_PATH.read_text(encoding="utf-8")
    de = DE_PATH.read_text(encoding="utf-8")

    for marker in (
        r"\Gamma\backslash\mathbb{H}^2",
        r"B(u)\in\mathrm{SO}^{+}(1,1)",
        r"\cite{Selberg1956}",
        r"\cite{Ungar2007}",
    ):
        assert en.count(marker) == 1
        assert de.count(marker) == 1
    assert "Selberg as a hyperbolic Lie-origin positive control" in en
    assert "Selberg als hyperbolischer Positivkontrollfall mit Lie-Ursprung" in de


def test_manuscripts_reject_strong_e10_and_cosmology_transfer():
    en = EN_PATH.read_text(encoding="utf-8")
    de = DE_PATH.read_text(encoding="utf-8")

    assert "full A--D/B' verification" in en
    assert "keine vollständige Verifikation von A--D/B'" in de
    assert "no cosmology statement, no UV completion" in en
    assert "keine Kosmologieaussage, keine UV-Vervollständigung" in de
    assert "Selberg satisfies E10" not in en
    assert "Selberg erfüllt E10" not in de

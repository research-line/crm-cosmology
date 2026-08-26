import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "results/paper5/METAPHOR_TRANSFER_INVARIANTS_2026-08-26.json"
EN_PATH = REPO_ROOT / "papers/extensions/Paper5_EN.tex"
DE_PATH = REPO_ROOT / "papers/extensions/Paper5_DE.tex"
EXPECTED_TERMS = {
    "saturation",
    "ferromagnetic",
    "cooperative",
    "renormalization",
    "temperature",
    "capacity",
}


def _audit():
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def test_audit_covers_exact_selector_terms_once():
    audit = _audit()
    terms = [entry["term"] for entry in audit["transfers"]]

    assert set(terms) == EXPECTED_TERMS
    assert len(terms) == len(set(terms)) == 6
    assert set(audit["scope_terms"]) == EXPECTED_TERMS


def test_every_transfer_records_preserved_and_lost_structure():
    for entry in _audit()["transfers"]:
        assert entry["source_domain"]
        assert entry["target_domain"]
        assert entry["mapping"]
        assert entry["preserved_invariants"]
        assert entry["not_preserved_or_not_derived"]
        assert entry["permitted_wording"]


def test_status_vocabulary_is_closed_and_only_normal_form_is_structural():
    audit = _audit()
    vocabulary = set(audit["status_vocabulary"])

    assert {entry["status"] for entry in audit["transfers"]} == vocabulary
    structural = [entry for entry in audit["transfers"] if entry["explicit_morphism"]]
    assert [(entry["term"], entry["status"]) for entry in structural] == [
        ("saturation", "STRUCTURAL_NORMAL_FORM")
    ]


def test_rg_transfer_remains_conditional_on_explicit_homomorphism():
    rg = next(entry for entry in _audit()["transfers"] if entry["term"] == "renormalization")

    assert rg["status"] == "CONDITIONAL_STRUCTURAL_GATE"
    assert rg["explicit_morphism"] is False
    assert "Pi(" in rg["mapping"]
    assert "theory_space_to_response_homomorphism" in rg["not_preserved_or_not_derived"]


def test_universality_boundary_refuses_wilsonian_or_microscopic_upgrade():
    boundary = _audit()["universality_boundary"]

    assert boundary["paper_v_result"] == "CONDITIONAL_ABEL_COLLAR_EQUIVALENCE_CLASS"
    assert boundary["wilsonian_universality_class_claim"] is False
    assert boundary["shared_microscopic_mechanism_claim"] is False
    assert boundary["external_QG_response_homomorphism_verified"] is False


def test_primary_source_registry_is_direct_and_https():
    sources = _audit()["source_registry"]
    external = [source for source in sources.values() if source["kind"] == "external_primary"]

    assert len(external) == 3
    assert all(source["url"].startswith("https://doi.org/") for source in external)


def test_bilingual_manuscripts_expose_same_new_invariants_and_references():
    en = EN_PATH.read_text(encoding="utf-8")
    de = DE_PATH.read_text(encoding="utf-8")

    for marker in (
        r"\label{tab:metaphor_invariants}",
        r"\label{eq:rg_response_homomorphism}",
        r"\bibitem{Yang1952}",
        r"\bibitem{WilsonKogut1974}",
    ):
        assert en.count(marker) == 1
        assert de.count(marker) == 1
    assert en.count(r"\label{tab:") == de.count(r"\label{tab:")
    assert en.count(r"\label{eq:") == de.count(r"\label{eq:")


def test_overstrong_metaphor_claims_are_removed_from_both_languages():
    en = EN_PATH.read_text(encoding="utf-8").lower()
    de = DE_PATH.read_text(encoding="utf-8").lower()

    assert "both systems satisfy an abel-type composition" not in en
    assert "structural rather than a mere metaphor" not in en
    assert "without cooperative reinforcement, there would be no classical spacetime" not in en
    assert "beide systeme erfüllen in der mean-field-approximation eine abel-artige" not in de
    assert "strukturell und nicht nur metaphorisch" not in de
    assert "ohne kooperative verstärkung gäbe es keine klassische raumzeit" not in de

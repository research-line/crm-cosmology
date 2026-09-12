"""Metadata, security, documentation, and Pfad B contract parity tests for crm-cosmology."""

from pathlib import Path
import tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_toml_structure():
    """Verify that pyproject.toml exists and contains valid metadata and PEP 621 classifiers."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml must exist"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    assert "project" in data
    project = data["project"]
    assert project.get("name") == "crm-cosmology"
    assert project.get("version") == "1.3.1"
    assert "description" in project
    assert project.get("requires-python") == ">=3.10"
    assert "license" in project
    assert project.get("license-files") == ["LICENSE", "NOTICE"]

    classifiers = project.get("classifiers", [])
    assert "Programming Language :: Python :: 3.12" in classifiers
    assert "Programming Language :: Python :: 3.13" in classifiers
    assert "Operating System :: OS Independent" in classifiers
    assert "Topic :: Scientific/Engineering :: Physics" in classifiers
    assert "Topic :: Scientific/Engineering :: Astronomy" in classifiers

    urls = project.get("urls", {})
    assert "Homepage" in urls
    assert "Repository" in urls
    assert "Documentation" in urls
    assert "Bug Tracker" in urls
    assert "Changelog" in urls
    assert "Security" in urls
    assert "Parent Organization" in urls
    assert "Umbrella Ecosystem" in urls
    assert "Third-Party Licenses" in urls
    assert "Marketing Log" in urls
    assert "LLM Ready" in urls
    assert "Zenodo DOI" in urls


def test_pep621_ecosystem_urls():
    """Verify that PEP 621 project URLs link to the research-line org, security policy, and open-bricks umbrella."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    urls = data.get("project", {}).get("urls", {})

    assert urls.get("Parent Organization") == "https://github.com/research-line"
    assert urls.get("Umbrella Ecosystem") == "https://github.com/open-bricks"
    assert urls.get("Security") == "https://github.com/research-line/crm-cosmology/blob/main/SECURITY.md"
    assert urls.get("Third-Party Licenses") == "https://github.com/research-line/crm-cosmology/blob/main/THIRD_PARTY_LICENSES.md"
    assert urls.get("Marketing Log") == "https://github.com/research-line/crm-cosmology/blob/main/MARKETING-LOG.txt"
    assert urls.get("LLM Ready") == "https://github.com/research-line/crm-cosmology/blob/main/llms.txt"


def test_llms_txt_structure_and_timestamp():
    """Verify that llms.txt contains required sections, canonical links, and current check timestamp."""
    llms_path = REPO_ROOT / "llms.txt"
    assert llms_path.exists(), "llms.txt must exist in repo root"
    content = llms_path.read_text(encoding="utf-8")

    assert "# Curvature Relaxation Model (CRM)" in content
    assert "## Last-checked: 2026-09-12" in content
    assert "## Canonical Links" in content
    assert "SECURITY.md" in content
    assert "THIRD_PARTY_LICENSES.md" in content
    assert "MARKETING-LOG.txt" in content
    assert "README_de.md" in content
    assert "## Summary" in content
    assert "## Interfaces & Reproduction Workflows" in content
    assert "## Safety & Governance Invariants" in content
    assert "## Search Phrases" in content
    assert "INV-DET-01" in content
    assert "INV-SLA-10" in content


def test_readme_and_readme_de_parity():
    """Verify that README.md and README_de.md are present with synchronized badges and cross-links."""
    readme_en = REPO_ROOT / "README.md"
    readme_de = REPO_ROOT / "README_de.md"

    assert readme_en.exists(), "README.md must exist"
    assert readme_de.exists(), "README_de.md must exist"

    en_content = readme_en.read_text(encoding="utf-8")
    de_content = readme_de.read_text(encoding="utf-8")

    # Both must reference each other
    assert "README_de.md" in en_content
    assert "README.md" in de_content

    # Both must link to standard project documents
    for doc in ["llms.txt", "SECURITY.md", "CHANGELOG.md", "THIRD_PARTY_LICENSES.md", "MARKETING-LOG.txt", "pyproject.toml"]:
        assert doc in en_content, f"Missing {doc} in README.md"
        assert doc in de_content, f"Missing {doc} in README_de.md"

    # Check status badges
    assert "Version-1.3.1-blue.svg" in en_content
    assert "Version-1.3.1-blue.svg" in de_content
    assert "LLM--Ready-2026--09--12" in en_content
    assert "LLM--Ready-2026--09--12" in de_content
    assert "Ecosystem-research--line-blue.svg" in en_content
    assert "Ecosystem-research--line-blue.svg" in de_content
    assert "Umbrella-open--bricks-purple.svg" in de_content
    assert "Zero--Egress" in en_content
    assert "Security%20SLA-48h%20Response%20%7C%205d%20Triage" in en_content


def test_readme_navigation_15_points_parity():
    """Verify that both READMEs contain all 15 quick navigation points with identical anchors."""
    en_content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    de_content = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    expected_anchors = [
        "quick-reference",
        "headline-scientific-results",
        "system-architecture--pipeline",
        "curated-verification-lifecycle",
        "governance--research-invariants",
        "core-papers--theoretical-series",
        "extension-papers--saturation-theorem",
        "mcmc-data-reproduction--datasets",
        "hi_class-patch-documentation",
        "sibling-research--ecosystem-matrix",
        "discovery--llm-context",
        "repository-structure",
        "testing--reproducibility",
        "third-party-licenses",
        "security--license",
    ]

    for anchor in expected_anchors:
        assert f"#{anchor}" in en_content, f"Missing anchor #{anchor} in README.md navigation"
        assert f"#{anchor}" in de_content, f"Missing anchor #{anchor} in README_de.md navigation"
        assert f'id="{anchor}"' in en_content, f"Missing anchor id='{anchor}' in README.md body"
        assert f'id="{anchor}"' in de_content, f"Missing anchor id='{anchor}' in README_de.md body"


def test_dual_mermaid_diagrams_parity():
    """Verify that both READMEs contain the system architecture flowchart and verification sequence diagram."""
    en_content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    de_content = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    # Flowchart diagram
    assert "flowchart TD" in en_content
    assert "flowchart TD" in de_content

    # Sequence diagram with autonumber
    assert "sequenceDiagram" in en_content
    assert "autonumber" in en_content
    assert "sequenceDiagram" in de_content
    assert "autonumber" in de_content


def test_governance_invariants_table_parity():
    """Verify that both READMEs contain the table of 10 Governance & Research Invariants."""
    en_content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    de_content = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    invariants = [
        "INV-DET-01",
        "INV-ZERO-02",
        "INV-USER-03",
        "INV-DATA-04",
        "INV-GATE-05",
        "INV-ARCH-06",
        "INV-PLAT-07",
        "INV-OPEN-08",
        "INV-LLM-09",
        "INV-SLA-10",
    ]

    for inv in invariants:
        assert inv in en_content, f"Missing {inv} in README.md"
        assert inv in de_content, f"Missing {inv} in README_de.md"


def test_sibling_research_matrix_parity():
    """Verify that all 16 sibling repositories are correctly linked in both README files."""
    en_content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    de_content = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    expected_slugs = [
        "abc-hct",
        "functional-stability-theory",
        "fst-nash",
        "prompt-archaeology-casestudy2",
        "connes-cvs",
        "rh-even-dominance",
        "economic-sanctions-coercive-diplomacy",
        "open-bricks",
        "decision-clicker",
        "clip-storyboard-director",
        "system-auditor",
        "safe-start-for-codex",
        "CultureEvolution",
        "WinStorePackager",
        "DokuZen",
        "UniversalDocsGrabber",
    ]

    for slug in expected_slugs:
        assert slug in en_content, f"Missing sibling {slug} in README.md"
        assert slug in de_content, f"Missing sibling {slug} in README_de.md"


def test_security_policy_sla_and_contacts():
    """Verify that SECURITY.md defines supported versions matrix, 48h response SLA, and ecosystem contacts."""
    sec_path = REPO_ROOT / "SECURITY.md"
    assert sec_path.exists(), "SECURITY.md must exist in repo root"
    content = sec_path.read_text(encoding="utf-8")

    assert "# Security Policy / Sicherheitsrichtlinie" in content
    assert "## English" in content
    assert "## Deutsch" in content
    assert "Supported Versions" in content
    assert "1.3.x" in content
    assert "48 hours" in content
    assert "48 Stunden" in content
    assert "5 business days" in content
    assert "5 Werktagen" in content
    assert "security@open-bricks.org" in content
    assert "open-science@research-line.org" in content
    assert "lukas@open-bricks.org" in content


def test_third_party_licenses_inventory():
    """Verify that THIRD_PARTY_LICENSES.md lists core libraries and zero-egress compliance."""
    lic_path = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert lic_path.exists(), "THIRD_PARTY_LICENSES.md must exist in repo root"
    content = lic_path.read_text(encoding="utf-8")

    assert "NumPy" in content
    assert "SciPy" in content
    assert "Matplotlib" in content
    assert "emcee" in content
    assert "CLASS / hi_class" in content
    assert "pytest" in content
    assert "Ruff" in content
    assert "Zero-Egress" in content
    assert "RunAsInvoker" in content


def test_marketing_log_audit_and_personas():
    """Verify that MARKETING-LOG.txt exists and contains the 4 personas, search keywords, and invariants."""
    mkt_path = REPO_ROOT / "MARKETING-LOG.txt"
    assert mkt_path.exists(), "MARKETING-LOG.txt must exist in repo root"
    content = mkt_path.read_text(encoding="utf-8")

    assert "crm-cosmology -- Marketing, Discoverability & Architecture Audit" in content
    assert "1. EXECUTIVE SUMMARY & VALUE PROPOSITION" in content
    assert "2. TARGET AUDIENCES & PERSONAS" in content
    assert "3. SEARCH PHRASES & DISCOVERABILITY KEYWORDS" in content
    assert "4. SIBLING ECOSYSTEM & PARTNER NETWORK MATRIX" in content
    assert "5. COMPETITIVE & MODEL COMPARISON MATRIX" in content
    assert "6. GOVERNANCE & RESEARCH INVARIANTS" in content
    assert "INV-DET-01" in content
    assert "INV-SLA-10" in content


def test_gitignore_hygiene_patterns():
    """Verify that .gitignore excludes synchronization conflicts, lockfiles, and raw data."""
    gi_path = REPO_ROOT / ".gitignore"
    assert gi_path.exists(), ".gitignore must exist"
    content = gi_path.read_text(encoding="utf-8")

    assert "data/raw/" in content
    assert "*-conflict-*" in content
    assert "*.sync-conflict-*" in content
    assert "*-WORKSTATION*" in content
    assert "*-ASUS-GEI*" in content
    assert "LOCK" in content
    assert ".ruff_cache/" in content
    assert ".pytest_cache/" in content


def test_changelog_recent_pfad_b_entry():
    """Verify that CHANGELOG.md contains release 1.3.0 with Pfad B additions."""
    cl_path = REPO_ROOT / "CHANGELOG.md"
    assert cl_path.exists(), "CHANGELOG.md must exist"
    content = cl_path.read_text(encoding="utf-8")

    assert "## [1.3.0] - 2026-09-11" in content
    assert "Discoverability, Marketing & Architecture Audit" in content
    assert "README_de.md" in content
    assert "THIRD_PARTY_LICENSES.md" in content
    assert "MARKETING-LOG.txt" in content


def test_ci_workflow_hardening():
    """Verify that CI workflow has timeout-minutes, concurrency, Python 3.13, and Ruff linting."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.exists(), "ci.yml must exist"
    content = ci_path.read_text(encoding="utf-8")

    assert "timeout-minutes: 15" in content
    assert "concurrency:" in content
    assert "cancel-in-progress: true" in content
    assert '"3.13"' in content
    assert "Lint with Ruff" in content
    assert "python -m ruff check ." in content
    assert "python -m pytest -ra -v" in content


def test_pep621_license_files_and_ruff_rules():
    """Verify PEP 621 license-files and comprehensive Ruff ruleset."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    assert data.get("project", {}).get("license-files") == ["LICENSE", "NOTICE"]
    ruff_select = data.get("tool", {}).get("ruff", {}).get("lint", {}).get("select", [])
    for rule in ["E", "F", "W", "B", "SIM", "C4", "RUF"]:
        assert rule in ruff_select, f"Missing {rule} in tool.ruff.lint.select"


def test_gitignore_multi_host_defense():
    """Verify that .gitignore guards against Workstation/Laptop conflict files, canonical locks, and build caches."""
    gi_path = REPO_ROOT / ".gitignore"
    content = gi_path.read_text(encoding="utf-8")

    assert "*-WORKSTATION-LG*" in content
    assert "*conflicted copy*" in content
    assert "* (Kopie)*" in content
    assert "* (Copy)*" in content
    assert "*.orig" in content
    assert "*.rej" in content
    assert "!package-lock.json" in content
    assert ".turbo/" in content
    assert ".nyc_output/" in content


def test_changelog_v131_pfad_a_entry():
    """Verify that CHANGELOG.md contains release 1.3.1 with Pfad A technical hygiene."""
    cl_path = REPO_ROOT / "CHANGELOG.md"
    content = cl_path.read_text(encoding="utf-8")

    assert "## [1.3.1] - 2026-09-12" in content
    assert "Technical Hygiene, CI Hardening & Metadata Modernization" in content

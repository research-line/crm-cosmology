import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_root_files_exist():
    """Verify that all standard root documents exist."""
    required_files = [
        "README.md",
        "README_de.md",
        "LICENSE",
        "CITATION.cff",
        "CHANGELOG.md",
        "llms.txt",
        "pyproject.toml",
        "requirements.txt",
        "SECURITY.md",
        "THIRD_PARTY_LICENSES.md",
        "MARKETING-LOG.txt"
    ]
    for filename in required_files:
        filepath = os.path.join(REPO_ROOT, filename)
        assert os.path.exists(filepath), f"Missing required file: {filename}"
        assert os.path.getsize(filepath) > 0, f"File is empty: {filename}"

def test_llms_txt_timestamp():
    """Verify that llms.txt has an up-to-date Last-checked header."""
    llms_path = os.path.join(REPO_ROOT, "llms.txt")
    with open(llms_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Last-checked: 2026-09-12" in content, "llms.txt Last-checked date is not updated to 2026-09-12"

def test_pyproject_metadata():
    """Verify that pyproject.toml contains required PEP 621 metadata."""
    pyproject_path = os.path.join(REPO_ROOT, "pyproject.toml")
    with open(pyproject_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert 'name = "crm-cosmology"' in content
    assert 'version = "1.3.1"' in content
    assert 'testpaths = ["tests"]' in content

def test_requirements_file():
    """Verify that requirements.txt lists core dependencies."""
    req_path = os.path.join(REPO_ROOT, "requirements.txt")
    with open(req_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "numpy" in content
    assert "scipy" in content
    assert "emcee" in content

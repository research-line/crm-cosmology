"""Automated manuscript integrity and publication artifact contract tests for crm-cosmology."""

from pathlib import Path
import re
import fitz

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "papers"

PAPERS = [
    ("Paper1_DE", 15),
    ("Paper1_EN", 14),
    ("Paper2_DE", 21),
    ("Paper2_EN", 20),
    ("Paper3_DE", 35),
    ("Paper3_EN", 23),
    ("Paper4_DE", 20),
    ("Paper4_EN", 19),
]


def test_manuscript_artifacts_presence_and_sizes():
    """Verify that all 8 canonical manuscript TeX files and PDFs exist and are non-empty."""
    assert PAPERS_DIR.is_dir(), "papers/ directory must exist"
    for stem, _min_pages in PAPERS:
        tex_path = PAPERS_DIR / f"{stem}.tex"
        pdf_path = PAPERS_DIR / f"{stem}.pdf"

        assert tex_path.is_file(), f"Missing TeX manuscript: {tex_path.name}"
        assert tex_path.stat().st_size > 50_000, f"TeX manuscript too small: {tex_path.name}"

        assert pdf_path.is_file(), f"Missing PDF publication: {pdf_path.name}"
        assert pdf_path.stat().st_size > 200_000, f"PDF file too small: {pdf_path.name}"


def test_manuscript_pdf_page_counts_and_textlayer():
    """Verify PDF page counts and ensure zero mojibake replacement characters."""
    total_pages = 0
    total_chars = 0

    for stem, min_pages in PAPERS:
        pdf_path = PAPERS_DIR / f"{stem}.pdf"
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        total_pages += page_count
        assert page_count >= min_pages, f"{stem}.pdf page count {page_count} < expected min {min_pages}"

        text = ""
        for page in doc:
            text += page.get_text()

        total_chars += len(text)
        assert "\ufffd" not in text, f"Mojibake character \\ufffd detected in {stem}.pdf"
        assert len(re.findall(r"\[\?\]", text)) == 0, f"Broken citation [?] detected in {stem}.pdf"

    assert total_pages >= 160, f"Total page count {total_pages} unexpectedly low"
    assert total_chars >= 600_000, f"Total text layer character count {total_chars} unexpectedly low"


def test_manuscript_tex_zero_sensitive_leaks():
    """Verify that no internal scratchpads, private proof notes or personal mail addresses leak into TeX files."""
    forbidden = [
        re.compile(r"BEWEISNOTIZ", re.IGNORECASE),
        re.compile(r"_proof-notes", re.IGNORECASE),
        re.compile(r"PROJEKTPLAN", re.IGNORECASE),
        re.compile(r"AKTIONSPLAN", re.IGNORECASE),
        re.compile(r"C:\\Users\\", re.IGNORECASE),
        re.compile(r"/Users/lukas", re.IGNORECASE),
        re.compile(r"lukas\.geiger@", re.IGNORECASE),
    ]

    for stem, _ in PAPERS:
        tex_path = PAPERS_DIR / f"{stem}.tex"
        content = tex_path.read_text(encoding="utf-8", errors="ignore")
        for pattern in forbidden:
            matches = pattern.findall(content)
            assert len(matches) == 0, f"Leak of pattern '{pattern.pattern}' found in {tex_path.name}"

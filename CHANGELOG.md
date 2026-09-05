# Changelog

All notable changes to the **Curvature Relaxation Model (CRM)** research repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to open-science preprint versioning tied to Zenodo archival records.

## [Unreleased]

### Changed
- **Local documentation and PDF text-quality audit (2026-09-05, base commit `2cd5401`):**
  - Normalized German guide, report, and runtime-facing text to real UTF-8 umlauts and `ß` while retaining intentional LaTeX accent macros in mathematical paper sources.
  - Rebuilt German Papers I--V with explicit ToUnicode font mappings; Paper VI was unchanged. `pdftotext` readback of all six `*_DE.pdf` files found no unexpected C0 control characters, U+FFFD replacement characters, or common mojibake markers.
  - Reconfirmed the distinct metadata roles without changing a release: Python package `1.2.4`; repository-pinned `CITATION.cff` archive v7.0 (`10.5281/zenodo.19233559`); main concept DOI `10.5281/zenodo.18728935`, which resolved on 2026-09-05 to published v8.4 (`10.5281/zenodo.21946248`). These audit changes remain local and unpublished.
  - Verified `4 passed` with `python -m pytest -q` and compiled `scripts/paper3/cfm_pantheonplus_test.py`. Long-running MCMC chains were not rerun; versioned chain summaries and scientific results were left unchanged.

## [1.2.4] - 2026-07-30

### Changed
- **Technical Hygiene & Maintenance Audit (2026-07-30):**
  - Updated `llms.txt` Last-checked header timestamp to `2026-07-30` and re-verified 4/4 Pytest unit tests 100% passing.
  - Updated `tests/test_crm_cosmology_structure.py` timestamp and version assertions.
  - Bumped version to `1.2.4` in `pyproject.toml` and test suite.

## [1.2.3] - 2026-07-29

### Changed
- **Technical Hygiene & Maintenance Audit (2026-07-29):**
  - Updated `llms.txt` Last-checked header timestamp to `2026-07-29` and re-verified 4/4 Pytest unit tests 100% passing.
  - Updated `tests/test_crm_cosmology_structure.py` timestamp and version assertions.
  - Bumped version to `1.2.3` in `pyproject.toml` and test suite.

## [1.2.2] - 2026-07-27

### Changed
- **Discoverability & Marketing Audit (2026-07-27):**
  - Updated `llms.txt` Last-checked header date to `2026-07-27` and added 4/4 Pytest test suite verification note.
  - Enhanced README header badges with CI build workflow status and Pytest suite badge.

## [1.2.1] - 2026-07-26

### Added
- **Technical Hygiene & Maintenance Audit (2026-07-26):**
  - Standardized PEP 621 `pyproject.toml` with project metadata, dependencies, and `[tool.pytest.ini_options]`.
  - Added automated GitHub Actions CI workflow (`.github/workflows/ci.yml`).
  - Added repository structure and metadata unit test suite (`tests/test_crm_cosmology_structure.py`).
  - Updated `llms.txt` header timestamp to `2026-07-26`.

### Changed
- **Discoverability & Marketing Audit (2026-07-25):**
  - Added Shields.io status badges for Python versions, Open Science, CC BY 4.0 license, Zenodo DOI, and LLM Indexing.
  - Added AI / LLM Agent Indexing callout note (`> [!NOTE]`) referencing `llms.txt`.
  - Added Mermaid system architecture & pipeline flowchart visualizing the theory-to-data workflow.
  - Standardized `llms.txt` header with `Last-checked: 2026-07-25` and enriched discovery search phrases.

## [1.2.0] - 2026-06-10

### Added
- Zenodo v7.0 record synchronization with DOI `10.5281/zenodo.19233559`.
- CITATION.cff metadata integration for reproducible citation.
- Extension Paper V (The Saturation Theorem) and Paper VI (QG-CRM) draft additions.

## [1.1.0] - 2026-03-16

### Added
- Route-3 scalar-vector successor action rebuild audit for Paper IV.
- SPARC galaxy rotation curve dataset integration.
- MCMC posterior analysis scripts for Pantheon+ SNe Ia and MOND checks.

## [1.0.0] - 2025-11-01

### Added
- Initial public open-science preprint repository release for CRM Papers I-IV.
- `hi_class` patch script `scripts/patch_cfm.py` for generic EFT proxy modeling.
- Planck 2018 TT+TE+EE spectrum comparison scripts and figures.

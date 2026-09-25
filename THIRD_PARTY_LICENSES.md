# Third-Party Licenses & Dependency Inventory

This document provides a comprehensive inventory of all third-party software libraries, mathematical engines, toolchains, and runtime environments utilized or referenced by **crm-cosmology** (`research-line/crm-cosmology`), including their respective licenses, copyright holders, and usage scopes.

Last updated: **2026-09-26** (Release `v1.3.2`)

---

## 1. Scientific Computing & MCMC Sampling Stack

### Python Standard Library
- **Project:** Python Software Foundation
- **Scope:** Runtime execution, numerical orchestration, multiprocess MCMC pool workers, test automation, and JSON/CSV certificate serialization
- **License:** Python Software Foundation License Version 2 (PSFL-2.0)
- **Copyright:** (c) 2001-2026 Python Software Foundation; All Rights Reserved.
- **Notice:**
  > Permission is hereby granted to copy, modify, and distribute this software and its documentation for any purpose and without fee, provided that the above copyright notice appear in all copies and that both that copyright notice and this permission notice appear in supporting documentation...

### NumPy
- **Project:** [NumPy](https://numpy.org/)
- **Scope:** Multidimensional array arithmetic, vector field discretization, matrix operations, and numerical integration
- **License:** BSD 3-Clause License
- **Copyright:** (c) 2005-2026, NumPy Developers. All rights reserved.

### SciPy
- **Project:** [SciPy](https://scipy.org/)
- **Scope:** Numerical integration (`scipy.integrate.quad`, `solve_bvp`, `odeint`), spline interpolation, and optimization
- **License:** BSD 3-Clause License
- **Copyright:** (c) 2001-2026, SciPy Developers. All rights reserved.

### Matplotlib
- **Project:** [Matplotlib](https://matplotlib.org/)
- **Scope:** Scientific visualization, CMB angular power spectra comparisons, MCMC posterior corner plots, and SPARC rotation curve figures
- **License:** Matplotlib License (PSF-based / BSD-compatible)
- **Copyright:** (c) 2002-2012 John D. Hunter; (c) 2012-2026 Matplotlib Development Team; All Rights Reserved.

### emcee
- **Project:** [emcee](https://emcee.readthedocs.io/)
- **Scope:** Affine-invariant ensemble Markov Chain Monte Carlo (MCMC) sampling for cosmological parameter estimation
- **License:** MIT License
- **Copyright:** (c) 2012-2026 Daniel Foreman-Mackey and contributors.

### CLASS / hi_class
- **Project:** [CLASS (Cosmic Linear Anisotropy Solving System)](https://lesgourg.github.io/class_public/class.html) & [hi_class](https://github.com/miguelzuma/hi_class_public)
- **Scope:** Linear cosmological perturbation theory solver in Horndeski gravity (`scripts/patch_cfm.py`)
- **License:** MIT-style / CLASS License
- **Copyright:** (c) Julien Lesgourgues, Thomas Tram, Miguel Zumalacarregui, et al.

---

## 2. Quality Assurance, Linting & Contract Tooling

### pytest
- **Project:** [pytest-dev/pytest](https://github.com/pytest-dev/pytest)
- **Scope:** Automated repository metadata, policy hygiene, scientific gatekeeper contracts, and numerical reproduction validation
- **License:** MIT License
- **Copyright:** (c) 2004-2026 Holger Krekel and pytest-dev contributors

### Ruff
- **Project:** [astral-sh/ruff](https://github.com/astral-sh/ruff)
- **Scope:** High-performance Python linter and code formatting validation across research pipelines and test harnesses
- **License:** MIT License / Apache License 2.0
- **Copyright:** (c) 2023-2026 Astral Software Inc.

---

## 3. Level 1 Software Bill of Materials (SBOM)

| Component | Scope / Usage | Type | License (SPDX) | Copyright Holder | Isolation & Egress Boundary |
|---|---|---|---|---|---|
| Python Standard Library | Numerical orchestration & CLI harness | Runtime | PSFL-2.0 | Python Software Foundation | 100% Offline / Local-First |
| NumPy | Multidimensional tensor & array math | Dependency | BSD-3-Clause | NumPy Developers | In-memory compute / Zero-Egress |
| SciPy | Numerical integration (BVP/ODE) | Dependency | BSD-3-Clause | SciPy Developers | In-memory compute / Zero-Egress |
| Matplotlib | Publication figure generation | Dependency | PSF-based / BSD | Matplotlib Development Team | Local file rendering / Zero-Egress |
| emcee | Affine-invariant MCMC ensemble | Dependency | MIT | Daniel Foreman-Mackey et al. | Multiprocess pool / Local-First |
| CLASS / hi_class | Boltzmann solver in Horndeski gravity | Solver | MIT-style (CLASS) | Julien Lesgourgues et al. | Subprocess C engine / Local-First |
| pytest | Automated contract verification | Tooling | MIT | Holger Krekel et al. | Local test runner / Zero-Egress |
| Ruff | Python linter & bytecode gatekeeper | Tooling | MIT / Apache-2.0 | Astral Software Inc. | Local static analysis / Zero-Egress |

---

## 4. Level 1 SBOM Invariant Cross-Reference Matrix

All dependencies and runtime components are strictly audited against the repository's 10 governance, architectural, and operational invariants:

| Invariant ID | Name | Architectural Guarantee | Dependency Scope | Audit Status |
|---|---|---|---|---|
| **`INV-DET-01`** | Deterministic Numerical Verification | Deterministic seeds, ODE tolerances, and proof scripts matching certificates | Python stdlib, NumPy, SciPy, emcee | Audited / Passed |
| **`INV-ZERO-02`** | 100% Offline & Zero-Egress Privacy | Complete offline execution with zero telemetry, background calls, or cloud APIs | Python stdlib, NumPy, SciPy, Matplotlib | Audited / Passed |
| **`INV-USER-03`** | Unprivileged Execution / RunAsInvoker | Strictly unprivileged user-mode execution without administrative elevation | Process runtime, GitHub Actions CI | Audited / Passed |
| **`INV-DATA-04`** | Curated Evidence Non-Pollution Boundary | Strict `.gitignore` boundaries isolating external raw datasets (`data/raw/`) | Git repository policy & `test_metadata.py` | Audited / Passed |
| **`INV-GATE-05`** | Fail-Closed Gate Architecture | Mathematical proof gates fail closed upon uncertainty; non-closed gates audited | `scripts/paper5/`, `tests/` | Audited / Passed |
| **`INV-ARCH-06`** | Bilingual Paper Series & Zenodo Archival | Preprints maintained in LaTeX & PDF across EN/DE, anchored to Zenodo DOIs | LaTeX compiler, Zenodo API/DOI | Audited / Passed |
| **`INV-PLAT-07`** | Cross-Platform Environment Parity | Identical execution across Windows, Linux (WSL), and macOS | Python `pathlib`, cross-platform CI | Audited / Passed |
| **`INV-OPEN-08`** | Permissive Open-Science CC-BY-4.0 & MIT | Unrestricted scholarly reuse, citation attribution, and open distribution | `LICENSE`, Zenodo archival | Audited / Passed |
| **`INV-LLM-09`** | Machine-Readable LLM Parity | Structured discovery via `llms.txt` and 18-point bilingual navigation | `llms.txt`, `README.md`, `README_de.md` | Audited / Passed |
| **`INV-SLA-10`** | 48-Hour Security Response & 5-Day Triage | Committed response window for vulnerability reporting | `SECURITY.md`, GitHub Advisories | Audited / Passed |

---

## 5. Observational Datasets (Attribution & Citation)

### Planck 2018 Legacy Archive
- **Scope:** CMB temperature, polarization, and lensing power spectra (TT+TE+EE)
- **Citation:** Aghanim et al. (Planck Collaboration), A&A 641, A6 (2020), [arXiv:1807.06209](https://arxiv.org/abs/1807.06209)

### Pantheon+ Supernova Sample
- **Scope:** Type Ia supernova distance moduli and covariance matrices
- **Citation:** Scolnic et al., ApJ 938, 113 (2022), [arXiv:2112.03863](https://arxiv.org/abs/2112.03863)

### SPARC (Spitzer Photometry & Accurate Rotation Curves)
- **Scope:** 171 disk galaxies with extended HI/Halpha rotation curves and 3.6 um surface photometry
- **Citation:** Lelli, McGaugh & Schombert, AJ 152, 157 (2016), [arXiv:1606.09251](https://arxiv.org/abs/1606.09251)

---

## 6. Compliance & Governance Assurance

1. **Permissive Open-Science Licensing**: All original research code, scripts, verification harnesses, and documentation in this repository are licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) and MIT-compatible terms, facilitating open science and unrestricted scholarly reproducibility.
2. **Offline Local-First Execution**: All cosmological computations, MCMC sampling runs, and test suites execute strictly locally with zero outbound network egress.
3. **Zero-Egress & Privacy**: No calculation telemetry, analytics, tracking tokens, or private research logs are transmitted outside the local machine.
4. **Unprivileged Non-Elevation (`RunAsInvoker`)**: All tools and scripts run under standard unprivileged user accounts (`RunAsInvoker`) without requiring administrative or root elevation.
5. **Curated Boundary Discipline**: Internal working notes (`BEWEISNOTIZ*.md`, `PLAN*.txt`) and raw downloaded data snapshots (`data/raw/`) remain isolated by strict `.gitignore` rules, ensuring version control contains only vetted, reproducible certificates.
6. **Zero-Copyleft Isolation Guarantee**: All software dependencies are distributed under permissive BSD-3-Clause, MIT, PSF, or Apache-2.0 licenses. There is zero viral copyleft contagion into the research codebase or derivative user workflows.
7. **System & Research Invariant Verification**: Full architectural conformity is verified against all 10 governance invariants (`INV-DET-01` through `INV-SLA-10`).
8. **Attribution & Notice**: Canonical copyright notices and institutional attribution are documented in [`NOTICE`](NOTICE).

# Contributing to crm-cosmology / Mitwirken an crm-cosmology

[English](#english) | [Deutsch](#deutsch)

---

<a id="english"></a>
## English

Thank you for your interest in contributing to **crm-cosmology** (`research-line/crm-cosmology`), an open-science computational cosmology research program developing the Curvature Relaxation Model (CRM), modified-gravity simulations, and bilingual preprint series.

### 1. Architectural Principles & 10 Governance Invariants

All contributions must strictly adhere to our core architectural, security, and open-science invariants:

1. **Deterministic Numerical Verification (`INV-DET-01`)**: All MCMC seeds, ODE solver tolerances, numerical quadratures, and mathematical proof scripts must yield deterministic, reproducible results matching stored numerical certificates.
2. **100% Offline & Zero-Egress Privacy (`INV-ZERO-02`)**: Complete offline execution with zero outbound network calls, zero analytics or telemetry, and zero cloud API dependencies across all simulation pipelines and verification runs.
3. **Unprivileged Execution / RunAsInvoker (`INV-USER-03`)**: All scripts, MCMC likelihood harnesses, CLI utilities, and automated test suites operate strictly within non-elevated user-mode privilege boundaries without requiring administrative or root elevation (`sudo` / Administrator).
4. **Curated Evidence Non-Pollution Boundary (`INV-DATA-04`)**: Strict `.gitignore` boundaries ensure that external raw observational datasets (`data/raw/`), working scratchpads, and confidential internal research notes remain isolated from version control.
5. **Fail-Closed Gate Architecture (`INV-GATE-05`)**: Mathematical proof gates fail closed upon uncertainty; non-closed physical gates ($D'$) are explicitly documented and restricted.
6. **Bilingual Paper Series & Zenodo Archival (`INV-ARCH-06`)**: All research preprints are maintained synchronously in English and German in LaTeX source and compiled PDF, anchored to immutable Zenodo DOIs.
7. **Cross-Platform Environment Parity (`INV-PLAT-07`)**: The codebase operates identically across Windows, Linux (Ubuntu/WSL), and macOS using standard POSIX/Windows-resilient path semantics.
8. **Permissive Open-Science CC-BY-4.0 & MIT (`INV-OPEN-08`)**: Unrestricted scholarly reuse, citation attribution, and open-source scientific software distribution under CC-BY-4.0 and permissive stack terms.
9. **Machine-Readable LLM Parity (`INV-LLM-09`)**: Structured discovery through [`llms.txt`](llms.txt), prompt context indexing, and 18-point bilateral navigation anchors.
10. **48-Hour Security Response & 5-Day Triage (`INV-SLA-10`)**: Coordinated vulnerability disclosure commitments with guaranteed initial response within 48 hours and triage within 5 business days.

### 2. Plan D Local Development Workflow

In accordance with our cross-system architecture (Plan D), the local git repository at `C:\_Local_DEV\repos\crm-cosmology` serves as the authoritative **Source of Truth**. Development, testing, and commits must take place exclusively in the canonical local clone. Cloud mirrors (e.g., OneDrive) serve solely as gitless read projections.

```powershell
# Clone the canonical repository
git clone https://github.com/research-line/crm-cosmology.git C:\_Local_DEV\repos\crm-cosmology
cd C:\_Local_DEV\repos\crm-cosmology

# Create and activate a clean virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install package and scientific dependencies
pip install -e .
pip install -r requirements.txt
pip install pytest ruff

# Run the complete test suite
pytest -ra -v

# Run code style & hygiene verification
ruff check .

# Validate Python bytecode compilation
python -m compileall -q .
```

### 3. Version Freeze Discipline (`T-20260920-167562623`)

`crm-cosmology` operates under strict version-freeze discipline. Version identifiers (`1.3.2` in `pyproject.toml` and metadata) must not be arbitrarily incremented during routine maintenance. All enhancements, bug fixes, and hygiene adjustments are documented under `## [Unreleased]` in `CHANGELOG.md`.

### 4. Quality Gates

Before submitting a pull request or pushing commits, verify all local quality gates:

1. `pytest`: 100% green test execution across all numerical, gatekeeper, and metadata contract test suites.
2. `ruff check .`: Zero lint errors and formatting violations.
3. `python -m compileall -q .`: Zero bytecode compilation errors.
4. `git diff --check`: Zero trailing whitespace or line-ending anomalies.
5. `git diff -G"version = "` / `git diff -G'"version"'`: Zero unauthorized version bumps.

### 5. Statutory Notice (§ 521 BGB) & Liability Disclaimer

This software is provided free of charge as open-science research code. In accordance with statutory German law (§ 521 BGB - *Gefälligkeitsrecht*), liability for defects in quality and title is strictly limited to intentional misconduct (*Vorsatz*) and gross negligence (*grobe Fahrlässigkeit*).

### 6. Coordinated Vulnerability Disclosure & 48h Security SLA

Security issues must never be submitted via public GitHub issues. Please report vulnerabilities responsibly through private GitHub Security Advisories or directly to:
- `open-science@research-line.org`
- `security@research-line.org`
- `security@open-bricks.org`
- `support@lukasgeiger.com`
- `lukas@open-bricks.org`

Initial acknowledgement is guaranteed within 48 hours, followed by risk triage within 5 business days per [`SECURITY.md`](SECURITY.md).

---

<a id="deutsch"></a>
## Deutsch

Vielen Dank für dein Interesse an einer Mitwirkung bei **crm-cosmology** (`research-line/crm-cosmology`), einem rechnergestützten Open-Science-Kosmologie-Forschungsprogramm zur Entwicklung des Krümmungsrelaxationsmodells (CRM), modifizierten Gravitationssimulationen und zweisprachigen Preprint-Serien.

### 1. Architektur-Prinzipien & 10 Governance-Invarianten

Alle Beiträge müssen unsere verbindlichen Kern- und Governance-Invarianten strikt einhalten:

1. **Deterministische Numerische Verifikation (`INV-DET-01`)**: Alle MCMC-Seeds, ODE-Löser-Toleranzen, Quadraturen und mathematischen Beweisskripte müssen deterministische, reproduzierbare Ergebnisse liefern, die exakt mit den hinterlegten Zertifikaten übereinstimmen.
2. **100% Offline- & Zero-Egress-Datenschutz (`INV-ZERO-02`)**: Vollständige Offline-Ausführung ohne externe Netzwerkaufrufe, ohne Telemetrie und ohne Cloud-Abhängigkeiten in allen Simulations- und Prüfroutinen.
3. **Privilegierungsfreie Ausführung / RunAsInvoker (`INV-USER-03`)**: Alle Skripte, Likelihood-Sampler, CLI-Tools und Tests laufen strikt im unprivilegierten Benutzermodus (`RunAsInvoker`) ohne administrative Rechte (`sudo` / Administrator).
4. **Isolationsgrenze für Rohdaten & Notizen (`INV-DATA-04`)**: Strikte `.gitignore`-Grenzen isolieren externe Rohdatensätze (`data/raw/`), Arbeitsnotizen und vertrauliche Forschungsentwürfe zuverlässig von der Versionskontrolle.
5. **Fail-Closed-Gate-Architektur (`INV-GATE-05`)**: Mathematische Beweis-Gates schließen bei Unvollständigkeit oder Unsicherheit strikt ab (Fail-Closed); nicht-geschlossene Gates ($D'$) werden explizit dokumentiert.
6. **Zweisprachige Manuskript-Serie & Zenodo-Archivierung (`INV-ARCH-06`)**: Alle Arbeiten werden synchron in Deutsch und Englisch in LaTeX und als PDF gepflegt und über permanente Zenodo-DOIs archiviert.
7. **Plattformübergreifende Umgebungsparität (`INV-PLAT-07`)**: Identische Ausführbarkeit unter Windows, Linux (Ubuntu/WSL) und macOS durch robuste Pfadsemantik.
8. **Permissive Open-Science CC-BY-4.0 & MIT (`INV-OPEN-08`)**: Uneingeschränkte wissenschaftliche Nachnutzbarkeit, Zitationsattribution und offene Weiterverbreitung unter CC-BY-4.0.
9. **Maschinenlesbare LLM-Parität (`INV-LLM-09`)**: Strukturierte Auffindbarkeit über [`llms.txt`](llms.txt), RAG-Kontexte und 18-Punkte-Navigationsanker.
10. **48-Stunden-Sicherheits-SLA & 5-Tage-Triage (`INV-SLA-10`)**: Verbindliche Sicherheits-SLA mit Erstreaktion binnen 48 Stunden und Risikobewertung innerhalb von 5 Werktagen.

### 2. Plan D Lokaler Entwicklungsworkflow

Gemäß unserer systemweiten Architektur (Plan D) fungiert das lokale Git-Repository unter `C:\_Local_DEV\repos\crm-cosmology` als maßgebliche **Source of Truth**. Entwicklung, Tests und Commits erfolgen ausschließlich in diesem kanonischen Klon. Cloud-Spiegel (z. B. OneDrive) dienen ausschließlich als gitlose Leseprojektionen.

```powershell
# Kanonisches Repository klonen
git clone https://github.com/research-line/crm-cosmology.git C:\_Local_DEV\repos\crm-cosmology
cd C:\_Local_DEV\repos\crm-cosmology

# Virtuelle Umgebung einrichten und aktivieren
python -m venv .venv
.venv\Scripts\Activate.ps1

# Paket und Abhängigkeiten installieren
pip install -e .
pip install -r requirements.txt
pip install pytest ruff

# Gesamte Testsuite ausführen
pytest -ra -v

# Linter und statische Prüfung ausführen
ruff check .

# Bytecode-Kompilierung prüfen
python -m compileall -q .
```

### 3. Version-Freeze-Disziplin (`T-20260920-167562623`)

`crm-cosmology` unterliegt einer strikten Version-Freeze-Disziplin. Versionsbezeichner (`1.3.2` in `pyproject.toml` und Metadaten) dürfen bei Routine-Wartungen nicht erhöht werden. Sämtliche Anpassungen werden unter `## [Unreleased]` in `CHANGELOG.md` erfasst.

### 4. Qualitäts-Tore

Vor jedem Pull Request oder Push müssen alle lokalen Qualitäts-Tore grün sein:

1. `pytest`: 100% bestandene Tests in allen mathematischen, Gate- und Metadaten-Testsuiten.
2. `ruff check .`: 0 Flake8/Ruff-Warnungen oder Formatierungsfehler.
3. `python -m compileall -q .`: 0 Bytecode-Kompilierungsfehler.
4. `git diff --check`: 0 Whitespace- oder Zeilenende-Fehler.
5. `git diff -G"version = "` / `git diff -G'"version"'`: 0 unautorisierte Versionsänderungen.

### 5. Gesetzlicher Haftungsausschluss (§ 521 BGB)

Dieses Projekt wird unentgeltlich als Open-Science-Forschungssoftware bereitgestellt. Gemäß **§ 521 BGB** (Gefälligkeitsrecht) ist die Haftung für Sach- und Rechtsmängel auf **Vorsatz und grobe Fahrlässigkeit** beschränkt.

### 6. Koordinierte Schwachstellenmeldung & 48h Sicherheits-SLA

Sicherheitsrelevante Befunde dürfen nicht über öffentliche GitHub Issues gemeldet werden. Bitte nutze private GitHub Security Advisories oder folgende Kontaktadressen:
- `open-science@research-line.org`
- `security@research-line.org`
- `security@open-bricks.org`
- `support@lukasgeiger.com`
- `lukas@open-bricks.org`

Die Erstreaktion erfolgt verbindlich innerhalb von 48 Stunden, die Risikobewertung innerhalb von 5 Werktagen gemäß [`SECURITY.md`](SECURITY.md).

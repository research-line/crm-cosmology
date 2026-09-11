# Security Policy / Sicherheitsrichtlinie

[English](#english) | [Deutsch](#deutsch)

---

<a name="english"></a>
## English

### Security & Privacy Commitments

`crm-cosmology` is an open-science cosmological research repository within the `research-line` ecosystem. We maintain strict security, privacy, and scientific data integrity standards across all numerical calculation pipelines, MCMC likelihood samplers, and preprint manuscripts.

#### 1. Local-First & Zero-Egress Execution
- All cosmological simulation scripts (`scripts/`), MCMC estimation harnesses, and analysis routines execute **100% locally and offline**.
- The repository contains zero telemetry, zero background network calls, and zero external analytical tracking.

#### 2. Non-Elevation & Subprocess Isolation
- Scripts and verification harnesses run exclusively in **unprivileged user mode** (`RunAsInvoker`) without requiring administrative (`sudo` / Administrator) rights.
- Subprocess invocations (such as calling CLASS/hi_class or Python multiprocessing pools) are strictly bounded to repository-local relative paths.

#### 3. Research Confidentiality & Boundary Protection
- Internal working drafts, active proof logs (`BEWEISNOTIZ*.md`, `PLAN*.txt`), raw external datasets (`data/raw/`), and transient compute states are strictly filtered and excluded via `.gitignore`.
- Only vetted, finalized preprints, analysis figures, and machine-verifiable calculation certificates are admitted to the version control tree.
- Absolute host system paths and credential keys are systematically forbidden and guarded by automated repository policy tests.

#### 4. Deterministic Reproducibility & Result Verification
- Machine-readable result certificates and MCMC summaries are deterministically generated and verified through reproducible scientific pipelines.
- Test suites enforce syntactic, semantic, and structural parity across all public releases.

### Supported Versions / Unterstützte Versionen

| Version | Supported / Unterstützt | Notes / Anmerkungen |
|---|---|---|
| `1.3.x` | :white_check_mark: | Current active release line / Aktive Release-Linie |
| `< 1.3.0` | :x: | Legacy preview releases / Veraltete Vorschau-Stände |

### Reporting Security Concerns

If you discover any security, privacy, or leak vulnerabilities within this repository, please report them responsibly:

- **Primary Contact:** `open-science@research-line.org`
- **Secondary Contact:** `security@ellmos.ai`
- **Ecosystem Coordination:** `security@open-bricks.org`, `lukas@open-bricks.org`
- **Author Contact:** `support@lukasgeiger.com`
- **GitHub Security Advisories:** [Report a Vulnerability](https://github.com/research-line/crm-cosmology/security/advisories/new)

**Response SLA:** Initial acknowledgment within 48 hours, triage and assessment within 5 business days, with continuous updates throughout the remediation process.

Please do not open public issues for sensitive security or credential disclosures until coordinated disclosure has occurred.

---

<a name="deutsch"></a>
## Deutsch

### Sicherheits- & Datenschutz-Garantien

`crm-cosmology` ist ein Open-Science-Forschungsrepository für geometrische Kosmologie und modifizierte Gravitation im `research-line`-Ökosystem. Wir wahren strikte Sicherheits-, Vertraulichkeits- und wissenschaftliche Datenintegritätsstandards über alle numerischen Berechnungs-Pipelines, MCMC-Likelihood-Sampler und Preprint-Manuskripte.

#### 1. Local-First & Zero-Egress Ausführung
- Sämtliche Simulationsskripte (`scripts/`), MCMC-Schätzungsroutinen und Analysewerkzeuge laufen **100% lokal und offline**.
- Das Repository enthält keinerlei Telemetrie, keine Hintergrund-Netzwerkaufrufe und kein externes Tracking.

#### 2. Non-Elevation & Subprozess-Sicherheit
- Skripte und Verifikations-Harnesses arbeiten ausschließlich im **nicht-privilegierten Benutzermodus** (`RunAsInvoker`) ohne administrative Rechte (`sudo` / Administrator).
- Subprozess-Aufrufe (CLASS/hi_class oder Python Multiprocessing) sind strikt auf relative Repository-Pfade begrenzt.

#### 3. Forschungsintegrität & Vertraulichkeitsgrenzen
- Interne Arbeitsentwürfe, aktive Beweisnotizen (`BEWEISNOTIZ*.md`, `PLAN*.txt`), externe Rohdaten (`data/raw/`) und transiente Berechnungszustände werden durch `.gitignore` strikt isoliert.
- Nur geprüfte, finalisierte Manuskripte, Abbildungen und maschinenlesbare Ergebnis-Zertifikate werden in die Versionskontrolle übernommen.
- Absolute Systempfade des Hosts und Zugangsdaten sind verboten und werden durch automatisierte Richtlinien-Tests abgesichert.

#### 4. Deterministische Reproduzierbarkeit & Ergebnisprüfung
- Maschinenlesbare Resultatszertifikate und MCMC-Zusammenfassungen werden deterministisch generiert und über reproduzierbare wissenschaftliche Pipelines verifiziert.
- Testsuiten stellen syntaktische und strukturelle Parität über alle Releases sicher.

### Sicherheitsmeldungen

Sollten Sie Sicherheits-, Datenschutz- oder Informationsleck-Schwachstellen entdecken, bitten wir um verantwortungsvolle Meldung:

- **Primäre Kontaktadresse:** `open-science@research-line.org`
- **Sekundäre Kontaktadresse:** `security@ellmos.ai`
- **Ökosystem-Koordination:** `security@open-bricks.org`, `lukas@open-bricks.org`
- **Autor-Kontakt:** `support@lukasgeiger.com`
- **GitHub Security Advisories:** [Schwachstelle melden](https://github.com/research-line/crm-cosmology/security/advisories/new)

**Reaktions-SLA:** Erstbestätigung innerhalb von 48 Stunden, Triage und Risikobewertung innerhalb von 5 Werktagen, mit kontinuierlichen Status-Updates während des Behebungsprozesses.

Bitte eröffnen Sie keine öffentlichen Issues für vertrauliche Sicherheits- oder Leak-Meldungen vor Abschluss der koordinierten Behebung.

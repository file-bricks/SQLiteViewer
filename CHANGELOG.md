# Changelog

## [Unreleased]

### Added
- **Pfad A Technische Hygiene, CI-Matrix-Härtung, PEP 621 Standardisierung & Vertragstest-Erweiterung (Stand 2026-10-18):**
  - CI-Matrix-Härtung: `.github/workflows/source-platform-smoke.yml` erweitert um Python 3.10 Runner (`matrix.python-version = ["3.10", "3.11", "3.12"]`) zur aktiven Absicherung des deklarierten PEP 621 `requires-python = ">=3.10"` Floors sowie Integration eines automatisierten `ruff check .` Linting-Schritts.
  - Multi-Host- & Cloud-Sync-Schutz: `.gitignore` gehärtet gegen Duplikatkopien von Synchronisationsdiensten (`* (Kopie)*`, `* (kopie)*`, `* (Copy)*`, `* (copy)*`), Locking-Artefakte (`uv.lock`) und Test-/Coverage-Caches (`.wheel-smoke/`, `wheelhouse/`, `.tox/`).
  - PEP 621 Standardisierung in `pyproject.toml`: Erweiterung der Projekt-URLs um Ökosystem-Aliase (`"Parent Organization"` -> file-bricks, `"Umbrella Ecosystem"` -> open-bricks); Vereinheitlichung der Pytest-Dateimuster (`python_files = ["test_*.py", "*_smoke.py"]`) zur automatischen Erkennung headless Smoke-Tests.
  - Unterordner-README-Parität: Prüfung aller Unterordner auf DE/EN-README-Parität nach P-006 Stufe 1; Aufnahme des Befunds für `web_companion/` in `MARKETING-LOG.txt` für den P-006 Leerlauf-Sprachzug.
  - Vertragstest-Erweiterung: `tests/test_metadata.py` um 4 neue Contract-Tests (`test_pytest_configuration_unified_smoke_discovery`, `test_extended_gitignore_patterns`, `test_subfolder_readme_inventory_documented`, `test_marketing_log_section_8_pfad_a_20261018`) erweitert und Badge-Prüfung auf Stand 2026-10-18 gehärtet.
- **Pfad B Discoverability, Visual 4-View Topology & Level 1 SBOM Re-Audit (Stand 2026-10-11):**
  - Visual Four-View Topology: Standardized ASCII architectural projection in Section 3 of both `README.md` and `README_de.md` ([VIEW 1: TKINTER GUI, USER INPUT & CLI INTEGRATION], [VIEW 2: ATOMIC TRANSACTIONAL EXPORT & SERIALIZATION ENGINE], [VIEW 3: SQLITE3 CORE DRIVER & DDL SCHEMA INTROSPECTION], [VIEW 4: RUNASINVOKER NON-ELEVATION, ZERO-EGRESS & AUDIT INTEGRITY]) covering all 10 system invariants (`INV-LOCAL-01` to `INV-LOCAL-10`).
  - Bilateral Fast Navigation: Standardized 16-point anchor navigation (`<a id="sec-01"></a>` to `<a id="sec-16"></a>`) across English and German documentation.
  - Contributing Guidelines: Fully updated bilingual `CONTRIBUTING.md` specifying Plan D canonical workflow (`C:\_Local_DEV\repos\SQLiteViewer`), unprivileged RunAsInvoker mode, § 521 BGB statutory liability disclaimer, and 48-hour security response SLA (`support@lukasgeiger.com`).
  - PEP 621 Standardisierung in `pyproject.toml`: Added `Contributing` and `Level 1 SBOM (Plain Text)` URLs, added `CONTRIBUTING.md` to `license-files`.
  - Level 1 SBOM Companion Re-Audit: Updated `THIRD_PARTY_LICENSES.txt` (5-field plain text companion) and `THIRD_PARTY_LICENSES.md` to Stand 2026-10-11 with hardened dependency floors (`pytest>=9.1.1`, `ruff>=0.9.0`, `pyinstaller>=6.10.0`).
  - Badges & Context Recency: Synchronized Shields.io badges for tests (127 passed | 100% green), Verified (2026-10-11), Contributing Guidelines, and Level 1 SBOM; updated `llms.txt` Stand 2026-10-11 with Section 3 4-View topology and 127 tests baseline.
  - Contract Tests: Added automated contract tests in `tests/test_metadata.py` verifying ASCII 4-view topology parity, bilateral CONTRIBUTING guidelines, PEP 621 URLs, SBOM currency, and version freeze discipline (2.1.0 frozen).
- **Security & License Contract Audit (5-Felder-SBOM & CVE-2025-7117 Floor):**
  - Dependency-Floors & CVE-Schutz: `pyproject.toml` `[tool.pytest.ini_options]` `minversion` auf `>=9.1.1` gehärtet (Schutz vor CVE-2025-7117 / GHSA-6w46-j5rx-g56g); Toolchain-Spezifikation `requirements-dev.txt` angelegt mit `pytest>=9.1.1`, `ruff>=0.9.0`, `pyinstaller>=6.10.0`, `pyinstaller-hooks-contrib>=2024.0`, `altgraph>=0.17.4`, `packaging>=24.0` und `setuptools>=61.0`.
  - PEP 621 Metadaten & Support: `pyproject.toml` um `maintainers = [{ name = "Lukas Geiger", email = "support@lukasgeiger.com" }]`, `[project.optional-dependencies]` (dev, build) und Security Advisories URL (`https://github.com/file-bricks/SQLiteViewer/security/advisories/new`) erweitert.
  - 5-Felder-SBOM-Inventar: `THIRD_PARTY_LICENSES.txt` vollständig auf das kanonische Level 1 5-Felder-Schema (`Package:`, `License:`, `SPDX:`, `URL:`, `Notice:`) für Standardbibliothek (`python-stdlib`, `tkinter`, `sqlite3`), Build-/Dev-Toolchain (`pytest`, `pluggy`, `iniconfig`, `ruff`, `pyinstaller`, `altgraph`, `packaging`, `setuptools`) und Web-Companion umgestellt.
  - Sicherheitsrichtlinie & SLAs: `SECURITY.md` um zweisprachige Struktur, 48-Hour Acknowledgment SLA, 5-Business-Day Triage SLA und verifizierte Maintainer-Sicherheitskontakte (`security@open-bricks.org`, `security@ellmos.ai`, `support@lukasgeiger.com`, `lukas@open-bricks.org`) gehärtet.
  - Repository- & Gitignore-Hygiene: `.gitignore` gegen Secrets (`secrets.*`, `*.crt`, `*.pfx`, `*.cer`), Test-Artefakte (`pytest_out.txt`, `pytest*.txt`) und Cloud-Sync-Konflikte (`*.conflict`, `*-conflict-*`) abgesichert.
  - Vertragstest-Suite: `tests/test_security_license_contract.py` mit 8 hermetischen Contract-Tests implementiert (Dependency-Floors, pytest minversion, 5-Felder-SBOM, Security-Policy SLAs, Gitignore-Regeln, Secret-/Pfad-Hygiene, Lizenz-Parität, Local-First Invarianten).
- **Formal NOTICE & Attribution:** Added root `NOTICE` file documenting copyright, unprivileged execution (`RunAsInvoker`), air-gapped zero network egress (`INV-LOCAL-01`), § 521 BGB statutory liability limitation, and PSF-2.0 / Tcl-Tk license attributions.
- **CI Matrix & Workflow Hardening:**
  - Extended `.github/workflows/source-platform-smoke.yml` to trigger on both `main` and `master` branches, added `windows-latest` to runner matrix alongside `ubuntu-latest` and `macos-latest`, enforced job-level `timeout-minutes: 10`, concurrency cancellation, and added metadata contract test execution in CI.
  - Hardened `.github/workflows/stale.yml` with `timeout-minutes: 10` and concurrency cancellation guards.
  - Hardened `.github/workflows/welcome.yml` with `timeout-minutes: 5` and scoped concurrency cancellation guards.
- **PEP 621 Standardisierung:** Declared `license-files` in `pyproject.toml` (`LICENSE`, `NOTICE`, `THIRD_PARTY_LICENSES.md`, `THIRD_PARTY_LICENSES.txt`), added `Notice` URL in `[project.urls]`.
- **Pytest Configuration & Windows Defense:** Configured `minversion = "9.1.1"`, `addopts = "-ra -v --basetemp=.pytest_tmp"` to eliminate Windows junction permission errors, and explicit `norecursedirs` exclusion rules.
- **Multi-Host & Cloud Sync Defense:** Hardened `.gitignore` against synchronization artifacts (`*-WORKSTATION-LG*`, `*-ASUS*`, `*-LAPTOP*`, `*-Mac Studio*`, etc.) and system-wide lock patterns (`LOCK.user.*`, `LOCK.until.*`, `LOCK.condition.*`, etc.).
- **Automated Contract Tests:** Expanded `tests/test_metadata.py` with 4 new contract tests verifying `NOTICE` presence, `.gitignore` defense patterns, workflow hardening (timeout, concurrency, permissions), and PEP 621 license-files declarations (60/60 tests passing, 100% green).
- **PWA & Mobile-Icon-Suite:** Vollständiges Icon-Inventar (`mobile_icons/` und `web_companion/icons/`) integriert mit Favicon, Maskable Icons und Apple Touch Icons.

### Changed
- Configured `[tool.ruff]` linter in `pyproject.toml` and fixed unused imports/variables in `SQLiteViewer.py` and test modules (zero ruff lint warnings).
- Updated test badge in `README.md` and `README_de.md` to reflect 107 passing tests (100% green).
- Updated `llms.txt` Last-checked header to `2026-10-03` with 107 Pytest + 43 Node companion tests verified.

### Fixed
- **Microsoft Store Release 2.1.0.0 & Icon-Konsistenz (Stand 2026-10-30, T-20261027-399570452):**
  - CSV-Formelinjektion (`0777549`): `_csv_safe_value()` in `SQLiteViewer.py` und `exportToCsv()` in `web_companion/library.js` neutralisieren führende Tabellenformel-Zeichen (`=`, `+`, `-`, `@`, Tab/CR).
  - Store-Paketversion in `store_package.json` und `store_package/SQLite Viewer Pro/AppxManifest.xml` auf `2.1.0.0` (synchron zu `APP_VERSION = "2.1.0"` und `pyproject.toml`) angehoben.
  - Icon-Konsistenz-Gate (`WINDOWS_STORE_BUGFIX_POLICY.md` §7a): `SQLiteViewer.ico` (16..256px) und alle 42 `Square44x44Logo.targetsize-{16..256}[_altform-unplated|_altform-lightunplated].png`-Varianten in `store_assets/` aus `Square310x310Logo.png` mit sauberer Ecken-Transparenz harmonisiert; `resources.pri` ins MSIX-Paket integriert.
  - PyInstaller-Spec (`SQLiteViewer.spec`): `locales/translations.json` und `SQLiteViewer.ico` in `datas` aufgenommen.
- **Web/PWA-Companion Importgrenzen:** Lokale JSON-Importe werden vor dem Lesen auf 8 MiB begrenzt; der Exportvertrag akzeptiert höchstens 100 Spalten und 2.000 Ergebniszeilen. Überschreitungen erhalten eine lokalisierte Fehlermeldung, statt große Nutzlasten bis in Rendering und lokale Wiederherstellung zu übernehmen. Node-Vertragstests decken die Dateigröße sowie beide Strukturgrenzen ab; der Service-Worker-Cache wurde auf v5 erhöht.
- **Empty Table State & Export Action Cleanup:** `_load_tables()` bereinigt Tabellen- und Schema-Dropdowns, Spalten-/Zeilen-Caches und Export-Kontexte vollständig bei leeren Datenbanken (z. B. nach `DROP TABLE`), setzt Zeilenzähler zurück und deaktiviert Export-Aktionen.
- **Defensive Sort & Search Invariants:** `load_selected_table()` setzt ungültige Sortierspalten defensiv zurück; `_clear_search()` belässt den aktiven Tabellenzähler intakt beim Drücken von Escape; `_search_data()` validiert Limit defensiv.
- **SQL Editor Selection Execution:** `execute_sql()` führt bei aktiver Selektion im SQL-Editor gezielt den markierten Block aus, um SQLite `ProgrammingError` bei Mehrfachanweisungen zu vermeiden.
- **Decoupled Table Metadata Inspection:** `_get_table_info()` entkoppelt Spalten-, Zähl-, Index- und Fremdschlüssel-Prüfungen in isolierte Blöcke mit Cursor-Cleanup.
- **Filename Sanitization:** `export_csv()` und `export_json()` filtern unzulässige Sonderzeichen (`/\:*?"<>|`) aus Standard-Dateinamen.
- **Atomic Persistence & Translation Parity:** `_save_settings()` und `translator.py` (`_save_translations()`) sichern Konfigurationen atomar über temporäre Dateien; `manage_translations.py` unterstützt `--check` zur Validierung der 6-Sprachen-Parität (DE, EN, ES, ZH, JA, RU).

## [2.1.1] - 2026-09-18

### Added
- **Web-Companion Internationalization (SV-I18N-05):**
  - Zweisprachige Lokalisierungsschicht (`web_companion/i18n.js`) fuer Deutsch (DE) und Englisch (EN) mit Fallback-Kette (`locale -> en -> de -> key`).
  - Dynamischer Sprachwechsler (DE / EN) im Hero-Header mit automatischer Browser-Spracherkennung und lokaler Persistenz via `localStorage`.
  - Vollstaendige `data-i18n`-Deklaration aller Texte, Placeholders, Tooltips und ARIA-Labels im Web-Companion (`web_companion/index.html`).
  - Mehrsprachige Metadaten- und Zeilenzusammenfassung (`formatSourceSummary`) in `web_companion/library.js`.
  - Offline-Shell-Cache-Aktualisierung (`web_companion/sw.js`, Cache-Version `sqliteviewer-companion-v4`).
  - Umfassende Node.js Test-Suite (`web_companion/tests/i18n.test.mjs`) fuer Dictionary-Paritaet, Fallbacks, Parameter-Interpolation und DOM-Uebersetzung.

## [2.1.0] - 2026-09-14

### Added
- **16-Punkte wechselseitige zweisprachige Schnellnavigation:** Vollstaendige Paritaet zwischen `README.md` (EN) und `README_de.md` (DE) mit identischer Ankerstruktur.
- **Visuelle Systemarchitektur & Export-Lebenszyklus:** Mermaid-Flussdiagramm (`flowchart TD`) und Sequenzdiagramm (`sequenceDiagram` mit `autonumber`) unter strikter Einhaltung von `HOOK-BANNER-ASSET-01` (vollstaendig quotierte Kantenbeschriftungen und Knotentexte).
- **Zielgruppen-Personas & SEO-Entdeckbarkeit:** Konkrete Profile `[PERSONA-01]` bis `[PERSONA-04]` mit High-Intent-Suchphrasen fuer Entwickler, Analysten, Admins und Windows Store Anwender.
- **10-Dimensionen-Vergleichsmatrix:** Gegenueberstellung zu DB Browser for SQLite, DBeaver, SQLiteStudio und Cloud-SaaS-Tools entlang der Systeminvarianten `INV-LOCAL-01` bis `INV-LOCAL-10`.
- **Drittanbieter-Lizenzaudit:** `THIRD_PARTY_LICENSES.md` mit detailliertem SPDX-Audit fuer Python Standardbibliothek (`sqlite3`), Tkinter (`Tcl/Tk License`), Bestaetigung von null externen Runtime-Abhaengigkeiten und Zero-Copyleft-Garantie auf Nutzerdaten.
- **Lokales Marketing-Register:** `MARKETING-LOG.txt` im Projekt-Root zur Dokumentation von Positionierung, Zielgruppen, Store-Readiness und Release-Pruefungen.
- **PEP 621 Projekt-URLs:** `pyproject.toml` um `[project.urls]` fuer Dokumentation, LLM-Kontext, Lizenzaudit, Store und Issues sowie `addopts = "-ra -v"` erweitert.
- **Automatisierte Vertragstests:** Neue Testsuite `tests/test_metadata.py` zur Validierung von Banner-Schutz, Mermaid-Syntax, Sprachparitaet und Manifest-Konsistenz.

### Changed
- Shields.io Badges in `README.md` und `README_de.md` modernisiert (Python 3.10+, MIT, Microsoft Store ID `9P6H501XB8JT`, Zero Egress, RunAsInvoker, 48h SLA, Oekosystem `file-bricks` / `open-bricks`).
- `llms.txt` aktualisiert (Stand 2026-09-14, Testanzahl, Verknuepfung mit Personas, Invarianten und Lizenzaudit).
- Paket- und Modulversionen auf 2.1.0 harmonisiert.

## [2.0.1] - 2026-08-23

### Fixed
- **Store-Paket registrierte keinen Datenbank-Handler.** Das `AppxManifest.xml` deklarierte
  keine `uap:FileTypeAssociation`; eine aus dem Store installierte App erschien deshalb nicht
  unter „Öffnen mit" und ein Doppelklick auf eine `.db` startete sie nicht. Ergänzt: `.db`,
  `.sqlite`, `.sqlite3` sowie der Ausführungsalias `sqliteviewer.exe`.
  Die Auswertung von `sys.argv[1]` war bereits vorhanden und wird jetzt durch Tests festgehalten.
- **Falsche Paket-Identität im Repository.** `store_package.json` führte
  `Geiger.SQLiteViewer`, im Partner Center ist die App aber als `Geiger.SQLiteViewerPro`
  registriert (Produkt `9P6H501XB8JT`). Ein aus diesem Stand gebautes Paket hätte nicht zur
  veröffentlichten App gepasst. Korrigiert, `store_id` ergänzt.
- Versionsdrift behoben: `APP_VERSION` stand auf `2.0.0`, `pyproject.toml` auf `2.0.1`.

### Added
- `tests/test_cli_db_argument.py` — hält die Argument-Auswertung fest und prüft zusätzlich,
  dass die im Manifest deklarierten Endungen mit denen des Dateidialogs übereinstimmen.
  Bewusst ohne GUI-Instanziierung: `SqlViewer()` blockiert ohne Anzeige, statt zu scheitern.
- Sprachen `de-DE` und `en-US` im Paket hinterlegt.

### Changed
- Paketversion `2.0.0.0` → `2.0.1.0`; `MaxVersionTested` `10.0.19041.0` → `10.0.22621.0`.
- Manifest und Store-Icons werden aus `store_package.json` erzeugt (store-packager 2.2.0).

### Store
- Eingereicht am 2026-08-23, Submission `1152921505701721645`, Status `Certification`.

## [Unreleased]

### Added
- Standard PEP 621 `pyproject.toml` configuration with metadata, dependencies, and `pytest` settings.
- Test suite status badge (30 passing tests) and LLM-Ready badge added to `README.md` and `README_de.md`.
- GFM LLM note callouts (`> [!NOTE]`) added to `README.md` and `README_de.md`.

### Changed
- Updated `llms.txt` Last-checked header to `2026-07-27` and verified test suite assertions (30/30 passing pytest tests).

- `web_companion/library.js`: `sortRows(rows, columns, options)` — clientseitige Spalten-Sortierung als pure-logic-Funktion (DOM-frei). Sortiert numerisch oder per `localeCompare`, null-Werte stets zuletzt, unbekannte Spalte gibt unveränderte Kopie zurück. Sieben neue Tests in `web_companion/tests/library.test.mjs`.
- `web_companion/app.js`: Spaltensortierung per Klick auf Tabellenkopf — Event-Delegation auf `<thead>`, Sortierrichtung per Wiederholklick umkehren, Sort-Indikator (↑/↓) im aktiven Spaltenkopf, `aria-sort`-Attribut gesetzt, Tastatur-Bedienbarkeit (Enter/Leertaste) über `tabIndex` + `keydown`-Handler.
- `web_companion/style.css`: Stile für klickbare Spaltenköpfe (`cursor: pointer`, Hover-Hintergrund, Focus-Ring, `.sort-indicator` in Akzentfarbe).
- `web_companion/library.js`: `exportToCsv(columns, rows)` — erzeugt RFC-4180-konformes CSV für die aktuell sichtbaren Zeilen (CRLF-Trennung, Blob-Werte als lesbarer Text, Quoting bei Komma/Anführungszeichen/Zeilenumbrüchen, null → leeres Feld). Sechs neue Tests in `web_companion/tests/library.test.mjs`.
- `web_companion/`: neuer Button „CSV exportieren" im Ergebniszeilen-Panel — lädt die gefilterten sichtbaren Zeilen als `<datenbankname>.csv` herunter; Button bleibt deaktiviert bis ein Export geladen ist.
- German `README_de.md` with local-first usage, privacy context, comparison table, and SQLiteViewer search phrases.
- `web_companion/`: static offline-first viewer for `sqliteviewer-export-v1.json` with local file import, demo mode, row filtering, metadata cards, LocalStorage restore, manifest, service worker, and Node smoke tests.
- Three regression tests in `tests/test_execute_sql.py` covering sort-indicator propagation in search mode, redundant-binding double-sort prevention, and empty-table CSV export.
- `tests/source_platform_smoke.py`: headless smoke tests for Linux and macOS source installs — covers module import, export serialization, `_build_export_payload`, SQL execution, and identifier escaping via fake infrastructure (no display required).
- `.github/workflows/source-platform-smoke.yml`: CI matrix for `ubuntu-latest` and `macos-latest` running the smoke tests on every push/PR to `main`.
- `llms.txt` with canonical repository, use cases, key files, discovery phrases, and boundaries for LLM/search crawlers.
- Local release bundle workflow documented for the ignored `releases/` workspace; public source files stay lightweight.
- Application icon support in the Tk window.
- Optional startup argument for opening a database file directly.
- `RELEASES.md` documents the local release bundle layout.
- `SQLiteViewer.spec` is tracked for reproducible PyInstaller builds.
- Optional JSON companion export `sqliteviewer-export-v1.json` with source metadata, row limits, visible columns, and serialized result rows.
- `EXPORTFORMAT.md` documents the JSON export contract for desktop-to-web/mobile companion workflows.
- Reproducible Windows Store screenshot generation under `_WARTUNG/generate_store_screenshots.py`; generated screenshots stay in the ignored local `releases/windowsstore/screenshots/` workspace while `README/screenshots/main.png` is refreshed for GitHub.
- Local WACK notes remain in the ignored `releases/windowsstore/` workspace; public root docs now describe only the source-controlled workflow.

### Fixed
- `translator.py`: `TranslationSystem.t()` lieferte bei leeren Übersetzungs-Strings in `translations.json` (`""`) den leeren String statt des deutschen Fallback-Texts.

### Changed
- Updated `llms.txt` Last-checked timestamp to 2026-07-22 and verified marketing, SEO, and discoverability context.
- Internal platform plan now separates desktop database inspection from read-only Web/PWA review and keeps Android/iOS as export-first companion targets instead of native SQLiteViewer clones.
- README now links the German guide and expands discovery phrases for `file-bricks/SQLiteViewer`, Python/Tkinter SQLite browser searches, and SQLite Viewer Pro.
- `llms.txt` now records the 2026-06-12 marketing/discovery check and broader search/disambiguation notes.
- Public docs now describe the export-first PWA path as the implemented mobile/browser companion strategy; raw `.sqlite` parsing stays a later optional evaluation step.
- README is now English-first with a Start Here table, clearer local-first positioning, search/disambiguation context, and repaired German umlauts.
- README now embeds the existing GUI screenshot from `README/screenshots/main.png`.
- Repository URLs and community health files now point to `file-bricks/SQLiteViewer`.
- `START.bat` now forwards command-line arguments and reports missing Python cleanly.
- Store listings and Store metadata now reflect the current CSV/JSON export feature set and the active `file-bricks/SQLiteViewer` privacy/support links.
- Store listing and screenshot workflow notes now avoid requiring ignored release artifacts in the public repo.
- Community workflows now use `actions/stale@v10` and `actions/first-interaction@v3` with current input names.

### Fixed
- `tests/source_platform_smoke.py` bootstraps the project root into `sys.path` before the first import, so the documented direct smoke command `python tests/source_platform_smoke.py` now works outside `pytest` instead of failing with `ModuleNotFoundError: SQLiteViewer`.
- Web Companion zeigt den vollständigen lokalen `database_path` nicht mehr in der sichtbaren Shell-Zusammenfassung; dort stehen jetzt Datenbankname und ein Hinweis, dass der volle Pfad im Export ausgeblendet wird.
- Exportaktionen zeigen jetzt klarer ihren aktiven Kontext an: Tabellenansicht und SQL-Ergebnis bekommen eigene CSV-/JSON-Beschriftungen, und leere Exportzustände sind direkt deaktiviert statt erst in einen Warn-Dialog zu laufen. Regressionen ergänzt in `tests/test_execute_sql.py`.
- SQL-Editor und Daten-Tab halten ihren Export-/View-State jetzt getrennt: `execute_sql()` schreibt Query-Ergebnisse nicht mehr in den Data-Tab-State, sondern in eigene `sql_result_*`-Felder; Exporte wählen abhängig vom aktiven Kontext den passenden Snapshot. Regressionen ergänzt in `tests/test_execute_sql.py` und `tests/source_platform_smoke.py`.
- `_search_data` now fetches column names via `PRAGMA table_info()` instead of relying on `self.current_columns`. After running a SQL query in the SQL Editor, `current_columns` reflected the query result columns rather than the actual table columns, causing a silent `Suchfehler: no such column: ...` whenever the search box was used afterwards. Three regression tests added (`tests/test_bugsweep_20260627.py`).
- Web companion metadata cards now render imported export metadata as inert text instead of interpolating it into `innerHTML`.
- Sorting an active table search now keeps the filtered result set and export context intact instead of jumping back to the full unfiltered table.
- Toolbar now uses a visible `Suche:` label instead of an icon-only search hint, and the refresh action is labeled consistently as `Aktualisieren` in the German UI.
- SQL Editor now detects result-returning statements via `cursor.description`, so
  queries with leading comments are rendered correctly instead of being treated as DML.
- SQL Editor now refreshes the currently selected table after data-changing
  statements instead of jumping back to the first table in the database.
- Search now escapes `%`, `_`, and `\` correctly so literal LIKE searches do not
  fail on wildcard-containing terms.
- Opening a database now only closes the current session after the new read-only
  connection succeeds, so failed open attempts keep the existing database in place.
- Sort indicator (↑/↓) was absent from column headings when viewing a search result — `_search_data` now adds the indicator to column headings when a sort column is active.
- Double sort triggered by a redundant `<Button-1>` binding combined with the Treeview `heading command` — removed the explicit binding; `heading command` alone handles sorting.
- `export_csv` blocked empty-table exports with a "no data" warning — now exports a header-only file consistently with `export_json`.

## [2.0.0] - 2026-02-01

### Added
- SQL Editor with syntax highlighting and query execution
- Schema view with CREATE TABLE inspection
- Full-text search across all columns
- CSV export functionality
- Column sorting (click headers)
- Keyboard shortcuts (Ctrl+O, Ctrl+F, Ctrl+E, F5, F9)
- Dark theme for code editors
- Table info display (row count, indexes, foreign keys)

### Changed
- Complete rewrite from basic viewer to full-featured browser
- Upgraded UI with notebook tabs (Data, Schema, SQL)
- Improved identifier escaping for safe SQL operations

## [1.0.0] - 2024-12-01

### Added
- Initial release
- Basic table browser with Treeview
- Database open dialog
- Row limit control
- Refresh functionality

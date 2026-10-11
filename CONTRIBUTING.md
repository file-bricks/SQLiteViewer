# Beitragsrichtlinie / Contributing Guide

## Deutsch

Vielen Dank für Ihr Interesse, zu **SQLiteViewer** beizutragen!

### System-Invarianten & Architekturprinzipien

Jeder Beitrag muss zwingend den 10 System-Invarianten der `file-bricks` / `open-bricks` Desktop-Familie entsprechen:
- **`INV-LOCAL-01` (Zero Network Egress):** 100% offline. Keine Telemetrie, keine HTTP-Aufrufe, keine Analytics-Tracker.
- **`INV-LOCAL-02` (Unprivilegierte Ausführung):** Strikte Ausführung unter Standard-Nutzerrechten (`RunAsInvoker`). Niemals UAC-Elevation erzwingen.
- **`INV-LOCAL-03` (Null externe Laufzeit-Abhängigkeiten):** Das Tool basiert ausschließlich auf der Python Standardbibliothek (`sqlite3`, `json`, `csv`, `pathlib`) und Tkinter.
- **`INV-LOCAL-04` (Nicht-destruktiver Standard):** Schreibgeschützte Erkundung als Standard; niemals versehentlich Nutzerdatenbanken mutieren.
- **`INV-LOCAL-05` (Kontextsensitiver Export):** Strukturierter Datenexport nach CSV und `sqliteviewer-export-v1.json`.
- **`INV-LOCAL-06` (Offline Web-Companion):** Begleitender Vanilla-JS-Viewer in `web_companion/` für browserbasierte lokale Analyse.
- **`INV-LOCAL-07` (Microsoft Store Paketierung):** Kompatibilität zum Windows Store Manifest (`9P6H501XB8JT`).
- **`INV-LOCAL-08` (100% Permissive Open Source):** Reine MIT-Lizenz ohne Copyleft-Klauseln auf Nutzerdaten oder DDL.
- **`INV-LOCAL-09` (Zweisprachige Parität EN/DE):** Vollständige wechselseitige Dokumentations- und Lokalisierungsparität.
- **`INV-LOCAL-10` (Sicherheits- & Schwachstellen-SLA):** Verbindliche 48-Stunden-Erstprüfungszusage für Sicherheitsmeldungen.

### Kanonische Entwicklungsumgebung (Plan D)

- **Source of Truth:** Lokaler Git-Klon unter `C:\_Local_DEV\repos\SQLiteViewer` (Branch `master`).
- **Cloud-Sync-Defense:** Keine Entwicklung direkt in synchronisierten Cloud-Ordnern (OneDrive), um Lock-Konflikte zu vermeiden.

### Wie Sie beitragen können

1. **Bug melden:** Erstellen Sie ein Issue mit dem Label `bug`.
2. **Feature vorschlagen:** Erstellen Sie ein Issue mit dem Label `enhancement`.
3. **Code beitragen:** Erstellen Sie einen Pull Request gegen den `master`-Branch.

### Pull Requests & Verifikation

1. Forken Sie das Repository auf GitHub.
2. Erstellen Sie einen Feature-Branch: `git checkout -b feature/mein-feature`.
3. Führen Sie die Tests und den Linter lokal aus:
   ```bash
   pytest -ra -v
   ruff check .
   ```
4. Committen Sie Ihre Änderungen: `git commit -m "feat(scope): prägnante Beschreibung"`.
5. Pushen Sie den Branch und erstellen Sie einen Pull Request.

### Haftungsausschluss (§ 521 BGB)

Dieses Projekt ist eine unentgeltliche Open-Source-Schenkung im Sinne der §§ 516 ff. BGB. Die Haftung des Urhebers ist gemäß § 521 BGB auf Vorsatz und grobe Fahrlässigkeit beschränkt.

### Sicherheitskontakt (48h SLA)

Sicherheitsrelevante Schwachstellen bitte vertraulich an `support@lukasgeiger.com` oder via GitHub Security Advisories melden.

---

## English

Thank you for your interest in contributing to **SQLiteViewer**!

### System Invariants & Architectural Principles

All contributions must strictly adhere to the 10 foundational system invariants of the `file-bricks` / `open-bricks` desktop family:
- **`INV-LOCAL-01` (Zero Network Egress):** 100% offline. Zero telemetry, zero analytics tracking, zero outbound network calls.
- **`INV-LOCAL-02` (Unprivileged Execution):** Executes strictly under standard user rights (`RunAsInvoker`). No administrative elevation.
- **`INV-LOCAL-03` (Zero External Runtime Dependencies):** Relies solely on Python's Standard Library (`sqlite3`, `json`, `csv`, `pathlib`) and Tkinter.
- **`INV-LOCAL-04` (Non-Destructive Default):** Safe, read-only exploration by default. Never mutate user databases without explicit action.
- **`INV-LOCAL-05` (Context-Aware Dual Export):** Contextual export to standard CSV and structured `sqliteviewer-export-v1.json`.
- **`INV-LOCAL-06` (Offline Web Companion):** Zero-dependency browser companion in `web_companion/` for local dataset inspection.
- **`INV-LOCAL-07` (Standard Store Packaging):** Clean AppX/MSIX manifest compatibility with verified Store ID `9P6H501XB8JT`.
- **`INV-LOCAL-08` (100% Permissive Open Source):** Pure MIT License with zero copyleft encumbrance on user databases or pipelines.
- **`INV-LOCAL-09` (Bilingual Parity EN/DE):** Complete reciprocal documentation and user interface localization.
- **`INV-LOCAL-10` (Security & Vulnerability SLA):** Documented 48-hour response SLA for security disclosures.

### Canonical Development Workflow (Plan D)

- **Source of Truth:** Local Git clone at `C:\_Local_DEV\repos\SQLiteViewer` (branch `master`).
- **Cloud Sync Isolation:** Avoid developing directly in cloud-synchronized folders (OneDrive) to prevent filesystem lock contention.

### How to Contribute

1. **Report bugs:** Open an issue with the `bug` label.
2. **Suggest features:** Open an issue with the `enhancement` label.
3. **Contribute code:** Submit a Pull Request targeting the `master` branch.

### Pull Requests & Verification

1. Fork the repository on GitHub.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Verify test suite and code formatting locally:
   ```bash
   pytest -ra -v
   ruff check .
   ```
4. Commit your changes: `git commit -m "feat(scope): concise description"`.
5. Push the branch and open a Pull Request.

### Liability & Warranty Disclaimer (§ 521 BGB)

This project is an unpaid open-source donation. Liability is strictly limited to intent and gross negligence pursuant to § 521 German Civil Code (BGB).

### Security Disclosures (48h SLA)

Please report security vulnerabilities confidentially to `support@lukasgeiger.com` or via GitHub Security Advisories.

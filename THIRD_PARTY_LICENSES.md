# Third-Party Licenses & Runtime Invariants

**Repository:** `file-bricks/SQLiteViewer`  
**Stand:** 2026-09-14  
**Version:** 2.1.0  
**SPDX-License-Identifier:** MIT  
**Application Title:** SQLite Viewer Pro  
**Store ID:** `9P6H501XB8JT`  
**Identity Name:** `Geiger.SQLiteViewerPro`  
**Umbrella Ecosystem:** `open-bricks` / `file-bricks`  

---

## 1. Overview & Compliance Architecture

`SQLiteViewer` is an open-source, local-first desktop SQLite database browser for Windows, Linux, and macOS. It is released under the permissive **MIT License**.

SQLiteViewer is built exclusively upon the **Python Standard Library** and standard desktop bindings (**Tkinter / Tcl/Tk**). It has **zero external runtime dependencies** (no pip packages required to run the core GUI or export data). All runtime components, packaging manifests, and development toolchains have been cataloged and audited for license compliance, unprivileged local execution, and zero-copyleft guarantees.

---

## 2. Dependency Inventory & SPDX Audit

### 2.1 Core Runtime Dependencies

| Package / Component | Declared Constraint | License (SPDX) | Type / Purpose | Copyleft Compliance |
|---|---|---|---|---|
| **Python Standard Library** | >= 3.10 | `PSF-2.0` | Core runtime (`sqlite3`, `json`, `csv`, `pathlib`, `os`, `sys`, `math`, `base64`) | Permissive (No copyleft, commercially usable) |
| **Tkinter (Tcl/Tk)** | Standard Python GUI | `Tcl/Tk License` (BSD-style) | Desktop windowing, ttk widgets, sortable Treeview, file dialogs | Permissive (No copyleft, unencumbered) |

### 2.2 Development, Testing & Quality Assurance

| Package / Component | Version | License (SPDX) | Type / Purpose | Copyleft? |
|---|---|---|---|---|
| **pytest** | >= 8.0.0 | `MIT` | Automated unit, regression, and metadata contract testing | No |
| **ruff** | >= 0.4.0 | `MIT OR Apache-2.0` | Static analysis, code formatting, and linting | No |

---

## 3. Zero-Copyleft Affirmation & User Data Protection

1. **Permissive Application Licensing:** SQLiteViewer is licensed under the MIT License.
2. **Zero Copyleft on User Databases:** User database files (`.db`, `.sqlite`, `.sqlite3`), schemas, custom SQL queries, query execution logs, and exported datasets (`.csv`, `sqliteviewer-export-v1.json`) remain the exclusive property of the user and are never tainted by copyleft obligations.
3. **No Network Egress:** SQLiteViewer executes completely offline without analytics, telemetry, phone-home mechanisms, or external API dependencies.
4. **Commercial and Homelab Friendly:** Permitted for unhindered use in academic, personal, commercial, and enterprise homelab environments.

---

## 4. System Invariants & Governance Compliance

SQLiteViewer strictly conforms to the 10 System Invariants of the `open-bricks` / `file-bricks` desktop portfolio:

| Invariant | Name | Specification & Implementation in SQLiteViewer |
|---|---|---|
| `INV-LOCAL-01` | **Zero Network Egress** | 100% offline execution. No socket communication, telemetry, pingbacks, or background cloud updates. |
| `INV-LOCAL-02` | **Unprivileged Execution** | Executes strictly in standard user context (`RunAsInvoker`). No administrator elevation required. |
| `INV-LOCAL-03` | **Zero External Runtime Dependencies** | Powered solely by Python standard library (`sqlite3`) and Tkinter. Zero pip packages required to run. |
| `INV-LOCAL-04` | **Non-Destructive File Association** | Default read-only inspection workflow. Double-clicking `.db`, `.sqlite`, `.sqlite3` opens files safely. |
| `INV-LOCAL-05` | **Context-Aware Dual Export** | Supports fast standard CSV export and rich structured JSON export (`sqliteviewer-export-v1.json`) with metadata. |
| `INV-LOCAL-06` | **Offline Browser Companion** | Includes standalone `web_companion/` enabling client-side inspection of exported JSON in any browser. |
| `INV-LOCAL-07` | **Standard Store Packaging** | Full AppX/MSIX manifest compatibility (`Geiger.SQLiteViewerPro`, Store ID `9P6H501XB8JT`). |
| `INV-LOCAL-08` | **100% Permissive Open Source** | Clean MIT License. Zero viral or copyleft contagion. |
| `INV-LOCAL-09` | **Bilingual Parity EN/DE** | 100% reciprocal documentation and UI internationalization (English & German). |
| `INV-LOCAL-10` | **Security & Vulnerability SLA** | Documented 48-hour response Service Level Agreement for security disclosures. |

---

## 5. Microsoft Store Compliance

- **Store ID:** `9P6H501XB8JT`
- **Application Name:** SQLite Viewer Pro
- **Package Identity:** `Geiger.SQLiteViewerPro`
- **Publisher:** `CN=52596601-BAB4-4F3F-B182-E8F3F273B202`
- **Execution Alias:** `sqliteviewer.exe`
- **Registered File Types:** `.db`, `.sqlite`, `.sqlite3`
- **Privacy Policy:** [`PRIVACY_POLICY.md`](PRIVACY_POLICY.md) (100% local processing, zero data collection)

# SQLiteViewer Web/PWA Companion

<p><b>English</b> | <a href="README_de.md">Deutsch</a></p>

The Web/PWA Companion provides a local, mobile- and browser-friendly read-only view for `sqliteviewer-export-v1.json`. It loads desktop exports directly in the browser, displays source metadata, SQL context, columns, and visible rows, and operates 100% offline-first.

## Purpose & Architecture

- **Zero Network Egress:** No server upload, no cloud sync, no external CDNs or telemetry.
- **Mobile & Browser Review Target:** Export-first companion for Android, iOS, tablet, and desktop browsers (per `PUBLICATION-POLICY.md` Rules **b**, **d**, and **f**).
- **Tier-2 6-Language UI (`i18n.js`):** Full localization across German (`de`), English (`en`), Spanish (`es`), Simplified Chinese (`zh`), Japanese (`ja`), and Russian (`ru`) with `localStorage` persistence.

## Automated Smoke & Contract Tests

Run the native Node.js test suite (46 tests across export schema, CSV formula safety, PWA manifest/SW, iOS safe-area insets, and 6-language parity):

```bash
npm test
```

From the repository root, the Python contract suite also validates the companion:

```bash
python -B -m pytest tests/test_web_companion.py -v
```

## Local Browser Preview

```bash
python -m http.server 4173
```

Open in a local browser:

- `http://127.0.0.1:4173/web_companion/`
- `http://127.0.0.1:4173/web_companion/?demo=1`

## Android / iOS PWA Smoke Procedure

1. Serve the companion over local HTTP/HTTPS.
2. Load `?demo=1` or an exported `sqliteviewer-export-v1.json` file.
3. **Android (Chrome):** Verify *Add to Home screen* installation and standalone launch.
4. **iOS (Safari):** Verify *Add to Home Screen* (`sqliteviewer-companion-180.png` icon, notch safe-area insets).
5. Switch the device offline and reopen to verify Service Worker (`sw.js`, `sqliteviewer-companion-v5`) offline shell recovery.

## Intentional Scope Boundaries

- Strictly read-only: no write-back into the desktop app or source SQLite database.
- Raw `.sqlite` parsing in the browser (WASM/`sql.js`) is an explicit non-goal for the export-first scope.
- Defensive local import limits: max `8 MiB` file size, `100` columns, and `2,000` result rows to guarantee responsive rendering and safe browser storage.
- **Provenance & Path Privacy (`source.database_path`):** Desktop exports retain `source.database_path` in the raw `sqliteviewer-export-v1.json` payload (and in local browser `localStorage` when auto-restore is used) for local provenance, whereas the Companion UI (`library.js` / `app.js`) intentionally displays only `source.database_name` without directory paths. Before sharing a raw JSON export externally, review or redact `source.database_path` if your local directory path is sensitive.

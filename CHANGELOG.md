# Changelog

## [Unreleased]

### Added
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

### Changed
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

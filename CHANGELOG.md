# Changelog

## [Unreleased]

### Added
- Local release bundle in `releases/v2.0.0/` refreshed from the current `dist/SQLiteViewer.exe` build.
- Application icon support in the Tk window.
- Optional startup argument for opening a database file directly.
- `RELEASES.md` documents the local release bundle layout.
- `SQLiteViewer.spec` is tracked for reproducible PyInstaller builds.

### Changed
- README now embeds the existing GUI screenshot from `README/screenshots/main.png`.
- Repository URLs and community health files now point to `file-bricks/SQLiteViewer`.
- `START.bat` now forwards command-line arguments and reports missing Python cleanly.

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

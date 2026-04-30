# RELEASES - SQLite Viewer Pro

Stand: 2026-04-29
Aktuelles lokales EXE-Bundle: `v2.0.0`

## Struktur

```text
releases/
├── v2.0.0/
│   ├── SQLiteViewer-2.0.0-win64.exe
│   ├── SQLiteViewer-2.0.0-source.zip
│   ├── CHANGELOG.txt
│   └── SHA256SUMS.txt
└── windowsstore/
    └── ...
```

## Aktueller Stand

- `dist/SQLiteViewer.exe` ist der frische lokale Build aus dem aktuellen Quellstand.
- `releases/v2.0.0/` enthält die versionierten GitHub-/Direktdownload-Artefakte.
- `releases/windowsstore/` bleibt getrennt für den MSIX-/Store-Workflow.
- Die Artefaktordner bleiben per `.gitignore` lokal; GitHub-Releases erhalten nur geprüfte Uploads.

## Letzte Pflege

- 2026-04-29: Lokales EXE-Bundle, Source-ZIP und Checksummen aus dem aktuellen Arbeitsstand aktualisiert.

# RELEASES - SQLite Viewer Pro

Stand: 2026-07-22
Lokales EXE-Bundle `v2.0.0`: Veröffentlichung gesperrt, siehe Provenienz.

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

- `releases/v2.0.0/SQLiteViewer-2.0.0-source.zip` hat eine zweifach verifizierte
  SHA-256, aber keine nachweisbare Zuordnung zu einem lokalen Git-Commit.
- Die dort behaltene EXE stimmt nicht mit der erwarteten EXE-Zeile in
  `SHA256SUMS.txt` überein, ist nicht signiert und darf weder als v2.0.0
  veröffentlicht noch durch einen neuen Hash stillschweigend legitimiert werden.
  Details und Wiederaufnahmebedingungen stehen in
  [`releases/v2.0.0/PROVENANCE.md`](releases/v2.0.0/PROVENANCE.md).
- `releases/windowsstore/` bleibt getrennt für den MSIX-/Store-Workflow.
- Die Artefaktordner bleiben per `.gitignore` lokal; GitHub-Releases erhalten nur
  nachweisbar geprüfte Uploads.

## Letzte Pflege

- 2026-04-29: Lokales EXE-Bundle, Source-ZIP und Checksummen aus dem damaligen Arbeitsstand aktualisiert.
- 2026-07-22: Erneute unabhängige SHA-256-Prüfung; EXE-Provenienzabweichung als
  Release-Block dokumentiert. Kein Neubuild, kein Austausch und kein Upload.

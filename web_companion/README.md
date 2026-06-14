# SQLiteViewer Web/PWA Companion

Der Companion ist die lokale, mobile und browserfreundliche Sicht auf
`sqliteviewer-export-v1.json`. Er lädt redigierte Desktop-Exporte im Browser,
zeigt Quelle, Query, Spalten und sichtbare Ergebniszeilen an und bleibt dabei
bewusst read-only.

## Ziel

- Kein Server-Upload und keine Cloud-Pflicht.
- Erste Companion-Linie für Android, iOS und Desktop-Browser.
- Export-first statt rohe `.sqlite`-Dateien im Browser, damit Datenschutz,
  Dateigröße und Komplexität klein bleiben.

## Lokaler Smoke

```bash
npm test
```

Das prüft:

- Export-Schema und Demo-Daten
- Filter- und BLOB-Darstellung
- Manifest, Icons und Offline-Shell

## Lokaler Browserlauf

```bash
python -m http.server 4173
```

Dann im Browser öffnen:

- `http://127.0.0.1:4173/web_companion/`
- `http://127.0.0.1:4173/web_companion/?demo=1`

## Android/iOS-PWA-Smoke

1. Companion lokal per HTTP bereitstellen.
2. `?demo=1` oder eine echte `sqliteviewer-export-v1.json` laden.
3. Android: in Chrome "Zum Startbildschirm hinzufügen" prüfen.
4. iOS: in Safari "Zum Home-Bildschirm" prüfen.
5. Offline erneut öffnen und Shell/Filter/Metadaten gegen den Service Worker validieren.

## Grenzen

- Keine Schreibfunktionen zurück in Desktop oder Datenbank
- Kein rohes `.sqlite`-Parsing im ersten Companion-Stand
- Keine Hintergrund-Synchronisation

Wenn später echte Nachfrage nach Browser-SQLite entsteht, kann ein
WASM-/`sql.js`-Pfad separat evaluiert werden. Für den aktuellen Usecase reicht
der Export-first-Companion.

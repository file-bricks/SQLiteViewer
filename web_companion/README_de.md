# SQLiteViewer Web/PWA-Companion

<p><a href="README.md">English</a> | <b>Deutsch</b></p>

Der Companion ist die lokale, mobile und browserfreundliche Read-only-Ansicht für `sqliteviewer-export-v1.json`. Er lädt Desktop-Exporte direkt im Browser, zeigt Quelle, SQL-Kontext, Spalten und sichtbare Ergebniszeilen an und arbeitet zu 100 % offline-first.

## Ziel & Architektur

- **Zero Network Egress:** Kein Server-Upload, kein Cloud-Zwang, keine externen CDNs und keine Telemetrie.
- **Review-Linie für Mobilgeräte & Browser:** Export-first-Companion für Android, iOS, Tablets und Desktop-Browser (gemäß `PUBLICATION-POLICY.md` Regeln **b**, **d** und **f**).
- **Tier-2 6-Sprachen-Oberfläche (`i18n.js`):** Vollständige Lokalisierung in Deutsch (`de`), Englisch (`en`), Spanisch (`es`), Vereinfachtem Chinesisch (`zh`), Japanisch (`ja`) und Russisch (`ru`) inklusive lokaler Sprachpersistenz.

## Automatisierter Smoke- & Vertragstest

Native Node.js-Testsuite ausführen (46 Tests für Export-Schema, CSV-Formelschutz, PWA-Manifest/Service-Worker, iOS-Safe-Area-Insets und 6-Sprachen-Parität):

```bash
npm test
```

Zusätzlich prüft die Python-Vertragstestsuite aus dem Repository-Root den Companion hermetisch:

```bash
python -B -m pytest tests/test_web_companion.py -v
```

## Lokaler Browserlauf

```bash
python -m http.server 4173
```

Anschließend im lokalen Browser öffnen:

- `http://127.0.0.1:4173/web_companion/`
- `http://127.0.0.1:4173/web_companion/?demo=1`

## Android-/iOS-PWA-Smoke

1. Companion lokal per HTTP/HTTPS bereitstellen.
2. `?demo=1` oder eine echte `sqliteviewer-export-v1.json` laden.
3. **Android (Chrome):** „Zum Startbildschirm hinzufügen" und Standalone-Start prüfen.
4. **iOS (Safari):** „Zum Home-Bildschirm" prüfen (`sqliteviewer-companion-180.png`, Safe-Area-Insets).
5. Offline erneut öffnen und Shell, Sprachumschaltung, Filter sowie Metadaten gegen den Service Worker (`sw.js`, `sqliteviewer-companion-v5`) validieren.

## Bewusste Systemgrenzen

- Keine Schreibfunktionen zurück in das Desktop-Programm oder die Ursprungsdatenbank.
- Kein rohes `.sqlite`-Parsing im Browser (WASM/`sql.js` bleibt für den aktuellen Export-first-Scope bewusst ausgeschlossen).
- Defensive lokale Importgrenzen: maximal `8 MiB` pro Datei, `100` Spalten und `2.000` Ergebniszeilen, damit Dateiimport, Tabellendarstellung und lokale Wiederherstellung auf Mobil- und Desktop-Browsern zuverlässig begrenzt bleiben.
- **Herkunftsnachweis & Pfad-Datenschutz (`source.database_path`):** Der Desktop-Export speichert `source.database_path` im Roh-JSON `sqliteviewer-export-v1.json` (sowie bei aktivierter Wiederherstellung lokal im Browser-`localStorage`) zur lokalen Herkunftsnachvollziehbarkeit, während die Companion-Oberfläche (`library.js` / `app.js`) sichtbar ausschließlich den Dateinamen `source.database_name` ohne Verzeichnispfad anzeigt. Vor einer externen Weitergabe der JSON-Datei sollte `source.database_path` bei sensiblen lokalen Verzeichnispfaden geprüft bzw. bereinigt werden.

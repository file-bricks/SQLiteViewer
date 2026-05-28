# Portierungsplan - SQLite Viewer Pro

Stand: 2026-05-27  
Scope: Windows Store, plattformübergreifende Desktop-Nutzung, Web-/Mobile-Companion

## Ausgangslage

SQLite Viewer Pro ist ein leichtgewichtiger SQLite-Datenbank-Browser auf Basis von Python, Tkinter und `sqlite3` aus der Standardbibliothek. Die Anwendung ist bereits als Windows-Desktop-App mit Store-Artefakten vorbereitet und laut README grundsätzlich für Windows, Linux und macOS geeignet.

Der Kernnutzen liegt im schnellen lokalen Öffnen, Durchsuchen, Abfragen und Exportieren von SQLite-Datenbanken. Die App verarbeitet lokale Datenbankdateien, oft mit potenziell sensiblen Inhalten. Deshalb bleibt ein offline-first Desktop-Modell wichtig; mobile und Web-Nutzung sollen primär kleine, bewusst importierte Datenausschnitte statt kompletter lokaler Datenbanken adressieren.

## Entscheidung

Windows Store bleibt der primäre Release-Kanal. macOS und Linux werden als Source-/Build-Smoke-Ziele aus derselben Tkinter-Codebasis geführt. Android, iOS und Web werden nicht als vollständige native Desktop-Clones geplant, sondern als Web/PWA-Companion für kleine SQLite-Dateien, Demo-Datenbanken und CSV-/JSON-Exporte.

Begründung:

- Nachfrage: SQLite ist ein Entwickler- und Power-User-Format; der größte Bedarf liegt weiter auf Desktop-Systemen mit lokalem Dateizugriff.
- Mobilität: Auf Mobilgeräten ist vollständiger Dateisystemzugriff eingeschränkt, aber das schnelle Prüfen kleiner Datenbankauszüge oder Exporte ist sinnvoll.
- Datenschutz: Lokale Datenbanken sollen ohne Cloud-Zwang geöffnet werden. Eine Web/PWA-Linie darf nur explizit ausgewählte Dateien oder Exporte verarbeiten.
- Aufwand: Die bestehende Tkinter-App ist für Desktop pragmatisch. Ein nativer Mobile-Clone würde viel UI- und Datei-Handling neu bauen, ohne den Kernnutzen stark zu erhöhen.

## Plattformbewertung

| Option | Bewertung | Entscheidung |
| --- | --- | --- |
| Windows Store | Sehr sinnvoll: Zielgruppe, bestehende MSIX-/Store-Artefakte und MIT-Lizenz passen. | P0 für Listing/Screenshots abgeschlossen; WACK-Protokoll bleibt im lokalen, ignorierten `releases/`-Workspace. |
| Android-Version oder Android-Clone | Native Vollversion nicht sinnvoll, weil SQLite-Dateizugriff und große Tabellen auf Mobilgeräten sperrig sind. | Nur PWA-Testziel für kleine Dateien/Exports. |
| Webapp | Sinnvoll als Companion: kleine `.sqlite`-Dateien im Browser öffnen, CSV/JSON ansehen, Demo-DBs prüfen. | P2: Web/PWA-Prototyp mit lokalem Browser-Speicher. |
| iOS-Version | Native App aktuell zu hoher Aufwand wegen Sandbox und App-Store-Review. | Nur PWA-Testziel nach Web-Prototyp. |
| Mac App | Sinnvoll als Source-/Build-Ziel, da Python/Tkinter portabel ist. | P3: macOS-Smoke-Test dokumentieren. |
| Linux-Version | Sinnvoll als Source-/Build-Ziel; optional später AppImage/Flathub prüfen. | P3: Linux-Smoke-Test dokumentieren. |

## Zielarchitektur

### Desktop-Kern

- Python/Tkinter bleibt die Desktop-Codebasis.
- SQLite-Dateien werden lokal und read-only geöffnet.
- CSV-Export bleibt das kleinste stabile Austauschformat.
- Optionales zusätzliches JSON-Exportformat `sqliteviewer-export-v1.json` ist für sichtbare Ergebnisse umgesetzt und transportiert Tabellenmetadaten, aktive Query, Spalten, Zeilenlimit und Ergebniszeilen.

### Web/PWA-Companion

- Separater Web-Prototyp, keine direkte Kopplung an Tkinter.
- Browser-seitige Verarbeitung kleiner Dateien über `sql.js` oder eine vergleichbare WebAssembly-SQLite-Engine.
- Keine Server-Uploads als Standard; der Datenschutz-Hinweis "lokal im Browser" soll sichtbar dokumentiert werden.
- Unterstützte Startfälle: Demo-DB öffnen, kleine `.sqlite` öffnen, CSV/JSON-Export anzeigen, Query-Ergebnis filtern.

### Export von Desktop zu Web/Mobile

- Kurzfristig CSV als vorhandener Exportpfad.
- `sqliteviewer-export-v1.json` ist als optionaler, stabiler Companion-Vertrag eingeführt.
- Keine Synchronisation vollständiger Datenbanken ohne separate Datenschutz- und Größenstrategie.

## Roadmap

### P0 - Store-Readiness

- Store-Screenshots sind jetzt reproduzierbar über `_WARTUNG/generate_store_screenshots.py` erzeugbar. Die generierten Store-Dateien bleiben lokal im ignorierten `releases/windowsstore/screenshots/`-Workspace; `README/screenshots/main.png` ist der source-kontrollierte GitHub-Screenshot.
- Store-Listing DE/EN ist gegen echte Umlaute, JSON-Export und aktuelle Support-/Privacy-Links synchronisiert.
- MSIX-/WACK-Testnotizen werden lokal im ignorierten `releases/windowsstore/`-Workspace gepflegt; der öffentliche Repo-Stand verweist nur auf source-kontrollierte Store- und Build-Helfer.

### P1 - Companion-Vertrag

- `sqliteviewer-export-v1.json` ist spezifiziert: App-Version, Quelle, Tabelle/Query, Spalten, Zeilen, Limit und Exportzeit sind dokumentiert.
- Desktop-Export ist optional neben CSV im Menü verfügbar.
- Datenschutzgrenzen für Companion-Dateien dokumentieren.

### P2 - Web/PWA-Prototyp

- Separaten `webapp/`-Prototyp erst bei Umsetzungsstart anlegen.
- Browser-seitiges Öffnen kleiner SQLite-Dateien evaluieren.
- Android/iOS über PWA-Installierbarkeit und Touch-Tabellenansicht testen.

### P3 - Desktop-Smoke-Tests

- Linux-Start aus Source mit Tkinter prüfen.
- macOS-Start aus Source mit Tkinter prüfen.
- Packaging für Linux/macOS nur nach belastbarer Nachfrage planen.

## Nicht-Ziele

- Kein nativer Android-/iOS-Clone in der ersten Portierungsphase.
- Kein Cloud-Datenbankservice.
- Kein automatischer Upload lokaler Datenbanken.
- Keine gemeinsame Desktop-/Mobile-Codebasis, wenn sie die einfache Tkinter-Desktop-App unnötig verkompliziert.

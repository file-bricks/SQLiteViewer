# SQLiteViewer

[English](README.md)

SQLiteViewer ist ein lokaler SQLite-Datenbank-Browser für Windows, Linux und macOS. Du öffnest `.db`-, `.sqlite`- oder `.sqlite3`-Dateien, prüfst Tabellen und Schema, führst SQL-Abfragen aus und exportierst sichtbare Daten als CSV oder JSON, ohne Datenbankinhalte hochzuladen.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-green)
![Plattform](https://img.shields.io/badge/Plattform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Schnellstart

| Bedarf | Einstieg |
|---|---|
| Lokale SQLite-Datenbank öffnen | `python SQLiteViewer.py pfad/zur/datenbank.sqlite` |
| Tabellen und Schema prüfen | Data-Tab und Schema-Tab |
| Eigene SQL-Abfrage ausführen | SQL-Editor öffnen, Abfrage schreiben, `F9` drücken |
| Sichtbare Daten exportieren | `File > Export as CSV` oder `File > Export as JSON` |
| Windows-Paket vorbereiten | `SQLiteViewer.spec`, `build_exe.bat`, `STORE_LISTING.md` |
| Maschinenlesbare Projektübersicht | [`llms.txt`](llms.txt) |

## Screenshot

![SQLiteViewer-Hauptfenster](README/screenshots/main.png)

Der Screenshot zeigt den Tabellen-Browser mit Schema- und SQL-Workflow-Tabs.

## Wofür das Tool gedacht ist

SQLiteViewer ist für schnelle lokale Prüfungen kleiner und mittlerer SQLite-Dateien gedacht: App-Datenbanken, Forschungsdaten, Test-Fixtures, Support-Snapshots und exportierte Arbeitsdaten. Der Fokus liegt bewusst auf einem schlanken, nachvollziehbaren Desktop-Workflow.

- **Lokal zuerst**: Datenbankdateien bleiben auf deinem Rechner.
- **Kein Konto**: kein gehostetes Backend, keine Telemetrie, kein Cloud-Sync.
- **Leichtgewichtig**: Python-Standardbibliothek plus Tkinter.
- **Exportierbar**: CSV für Tabellenkalkulationen, JSON für Companion-Workflows.
- **Einfach prüfbar**: eine zentrale Python-Datei plus dokumentierte Paketierungsdateien.

## Funktionen

- Tabellen-Browser mit sortierbarem Raster
- Schema-Ansicht für `CREATE TABLE`-Definitionen
- SQL-Editor mit Ergebnisansicht
- Suche über sichtbare Tabellenspalten
- CSV-Export für Tabellen oder Abfrageergebnisse
- JSON-Export als `sqliteviewer-export-v1.json`
- Start mit direktem Dateipfad
- Tastenkürzel: `Ctrl+O`, `Ctrl+F`, `Ctrl+E`, `F5`, `F9`

## Installation und Start

Voraussetzungen:

- Python 3.10 oder neuer
- Tkinter, bei den meisten Python-Installationen enthalten

Start aus dem Quellcode:

```bash
git clone https://github.com/file-bricks/SQLiteViewer.git
cd SQLiteViewer
python SQLiteViewer.py
```

Datenbank direkt öffnen:

```bash
python SQLiteViewer.py pfad/zur/datenbank.sqlite
```

Unter Windows kannst du auch `START.bat` doppelklicken.

## Nutzung

1. Datenbank über `File > Open Database`, `Ctrl+O` oder einen Startpfad öffnen.
2. Tabelle im Dropdown auswählen.
3. Suchfeld nutzen, um sichtbare Zeilen zu filtern.
4. Schema-Tab öffnen, um Tabellendefinitionen zu prüfen.
5. SQL-Editor öffnen, Abfrage schreiben und mit `F9` ausführen.
6. Sichtbare Daten als CSV oder JSON exportieren.

## Suchkontext

Dieses Repository ist `file-bricks/SQLiteViewer`: ein Python/Tkinter-Desktoptool für lokale SQLite-Inspektion, SQL-Abfragen, CSV-Export und JSON-Companion-Export. Es ist nicht DB Browser for SQLite, nicht DBeaver, keine Android-SQLite-App, keine iOS-Debug-Bibliothek und kein gehostetes Web-Admin-Panel.

Nützliche Suchphrasen:

- `file-bricks SQLiteViewer`
- `file-bricks/SQLiteViewer`
- `lokaler SQLite Viewer Python Tkinter`
- `SQLite Datenbank Browser CSV JSON Export`
- `offline SQLite Browser Windows Python`
- `SQLite Tabellen Browser SQL Editor Tkinter`
- `SQLite Viewer Pro Microsoft Store`

## Vergleich

| Funktion | SQLiteViewer | DB Browser for SQLite | DBeaver |
|---|:---:|:---:|:---:|
| Lokale SQLite-Dateien öffnen | Ja | Ja | Ja |
| SQL-Abfragen | Ja | Ja | Ja |
| Schema-Ansicht | Ja | Ja | Ja |
| CSV-Export | Ja | Ja | Ja |
| JSON-Companion-Export | Ja | Nein | Teilweise |
| Kern auf Python-Standardbibliothek | Ja | Nein | Nein |
| Schlanker Quellcode-Checkout | Ja | Teilweise | Nein |
| Kein Konto oder Backend | Ja | Ja | Ja |

## Datenschutz

SQLiteViewer öffnet lokale Datenbankdateien direkt über Python `sqlite3`. Das Tool verbindet sich nicht mit externen Diensten und überträgt keine Datenbankinhalte. Details stehen in der [`PRIVACY_POLICY.md`](PRIVACY_POLICY.md).

## Lizenz

[MIT](LICENSE)

## Haftung

Dieses Projekt ist eine unentgeltliche Open-Source-Schenkung im Sinne der §§ 516 ff. BGB. Die Haftung des Urhebers ist gemäß § 521 BGB auf Vorsatz und grobe Fahrlässigkeit beschränkt. Ergänzend gilt der Haftungsausschluss der MIT-Lizenz.

Nutzung auf eigenes Risiko. Keine Wartungszusage, keine Verfügbarkeitsgarantie, keine Gewähr für Fehlerfreiheit oder Eignung für einen bestimmten Zweck.

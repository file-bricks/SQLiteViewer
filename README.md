# SQLite Viewer Pro

Ein leichtgewichtiger, schneller SQLite-Datenbank-Browser mit Python und Tkinter. Oeffne, durchsuche und analysiere jede SQLite-Datenbank -- ohne SQL-Kenntnisse.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Funktionen

- **Tabellen-Browser** - Listet alle Tabellen mit sortierbarem Datenraster auf
- **Schema-Ansicht** - CREATE TABLE Statements mit Syntax-Highlighting anzeigen
- **SQL-Editor** - Eigene Abfragen mit Syntax-Highlighting und Ergebnisansicht ausfuehren
- **Volltextsuche** - Echtzeit-Suche ueber alle Spalten
- **CSV-Export** - Tabellen oder Abfrageergebnisse als CSV exportieren
- **Sortierung** - Spaltenkoepfe anklicken fuer auf-/absteigende Sortierung
- **Tastenkuerzel** - Ctrl+O (Oeffnen), Ctrl+F (Suche), Ctrl+E (Export), F5 (Aktualisieren), F9 (SQL ausfuehren)

## Screenshots

### Daten-Browser
Oeffne beliebige `.db`-, `.sqlite`- oder `.sqlite3`-Dateien und durchsuche Tabellen sofort.

### Schema-Ansicht
Tabellenstrukturen mit syntaxhervorgehobenen CREATE TABLE Statements anzeigen.

### SQL-Editor
SQL-Abfragen mit Echtzeit-Syntax-Highlighting schreiben und ausfuehren.

## Installation

### Voraussetzungen

- Python 3.10 oder hoeher
- Tkinter (bei den meisten Python-Installationen enthalten)

Keine zusaetzlichen Abhaengigkeiten -- nutzt ausschliesslich die Python-Standardbibliothek.

### Aus dem Quellcode starten

```bash
git clone https://github.com/lukisch/SQLiteViewer.git
cd SQLiteViewer
python SQLiteViewer.py
```

### Windows

Doppelklick auf `START.bat` oder:

```cmd
python SQLiteViewer.py
```

## Verwendung

1. **Datenbank oeffnen**: `File > Open Database` oder `Ctrl+O`
2. **Tabellen durchsuchen**: Tabelle aus dem Dropdown waehlen
3. **Suchen**: Im Suchfeld tippen, um Zeilen zu filtern
4. **Schema ansehen**: Zum Schema-Tab wechseln
5. **SQL ausfuehren**: Zum SQL-Editor-Tab wechseln, Abfrage schreiben, `F9` druecken
6. **Exportieren**: `File > Export as CSV` oder `Ctrl+E`

## Tastenkuerzel

| Kuerzel | Aktion |
|---------|--------|
| `Ctrl+O` | Datenbank oeffnen |
| `Ctrl+Q` | Beenden |
| `Ctrl+E` | CSV exportieren |
| `Ctrl+F` | Suchfeld fokussieren |
| `Ctrl+A` | Alle Zeilen markieren |
| `F5` | Tabelle aktualisieren |
| `F9` | SQL-Abfrage ausfuehren |

## Vergleich

| Funktion | SQLite Viewer Pro | DB Browser | DBeaver |
|----------|:-----------------:|:----------:|:-------:|
| Sofortiger Start | Ja | Langsam | Langsam |
| SQL-Abfragen | Ja | Ja | Ja |
| Tabellen durchsuchen | Ja | Ja | Ja |
| Schema-Ansicht | Ja | Ja | Ja |
| CSV-Export | Ja | Ja | Ja |
| Volltextsuche | Ja | Eingeschraenkt | Ja |
| Portabel | Ja | Teilweise | Nein |
| Leichtgewichtig | Ja | Nein | Nein |
| Keine Installation | Ja | Nein | Nein |

## Technische Details

- **Framework**: Tkinter + ttk
- **Datenbank**: sqlite3 (stdlib)
- **Abhaengigkeiten**: Keine (reines Python stdlib)
- **Einzelne Datei**: ~750 Zeilen Python

---

## English

A lightweight, fast SQLite database browser built with Python and Tkinter. Open, browse, search and query any SQLite database without SQL knowledge.

### Features

- **Table Browser** - Automatically lists all tables with sortable data grid
- **Schema View** - Inspect CREATE TABLE statements with syntax highlighting
- **SQL Editor** - Execute custom queries with syntax highlighting and result view
- **Full-Text Search** - Search across all columns in real-time
- **CSV Export** - Export any table or query result to CSV
- **Sorting** - Click column headers to sort ascending/descending
- **Keyboard Shortcuts** - Ctrl+O (open), Ctrl+F (search), Ctrl+E (export), F5 (refresh), F9 (execute SQL)

### Screenshots

#### Data Browser
Open any `.db`, `.sqlite`, or `.sqlite3` file and browse tables instantly.

#### Schema View
View table definitions with syntax-highlighted CREATE TABLE statements.

#### SQL Editor
Write and execute SQL queries with real-time syntax highlighting.

### Installation

#### Requirements

- Python 3.10 or higher
- Tkinter (included with most Python installations)

No additional dependencies required - uses only Python standard library.

#### Run from Source

```bash
git clone https://github.com/lukisch/SQLiteViewer.git
cd SQLiteViewer
python SQLiteViewer.py
```

#### Windows

Double-click `START.bat` or run:

```cmd
python SQLiteViewer.py
```

### Usage

1. **Open a database**: `File > Open Database` or `Ctrl+O`
2. **Browse tables**: Select a table from the dropdown
3. **Search**: Type in the search field to filter rows
4. **View schema**: Switch to the Schema tab
5. **Run SQL**: Switch to the SQL Editor tab, write a query, press `F9`
6. **Export**: `File > Export as CSV` or `Ctrl+E`

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open database |
| `Ctrl+Q` | Quit |
| `Ctrl+E` | Export CSV |
| `Ctrl+F` | Focus search |
| `Ctrl+A` | Select all rows |
| `F5` | Refresh table |
| `F9` | Execute SQL query |

### Comparison

| Feature | SQLite Viewer Pro | DB Browser | DBeaver |
|---------|:-----------------:|:----------:|:-------:|
| Instant startup | Yes | Slow | Slow |
| SQL queries | Yes | Yes | Yes |
| Browse tables | Yes | Yes | Yes |
| Schema view | Yes | Yes | Yes |
| CSV export | Yes | Yes | Yes |
| Full-text search | Yes | Limited | Yes |
| Portable | Yes | Partial | No |
| Lightweight | Yes | No | No |
| No install needed | Yes | No | No |

### Technical Details

- **Framework**: Tkinter + ttk
- **Database**: sqlite3 (stdlib)
- **Dependencies**: None (pure Python stdlib)
- **Single file**: ~750 lines of Python

## License

[MIT](LICENSE)

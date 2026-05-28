# Exportformat – `sqliteviewer-export-v1.json`

Stand: 2026-05-25

## Zweck

`sqliteviewer-export-v1.json` ist ein optionaler Companion-Export für Web/PWA-, Review- und Austausch-Workflows. CSV bleibt der Standardexport für einfache Tabellenweitergabe. JSON ergänzt diesen Pfad um Metadaten zur Herkunft und zur aktuell sichtbaren Ansicht.

## Grundsätze

- Der Export ist additiv: CSV bleibt unverändert verfügbar.
- Es werden nur aktuell sichtbare Ergebniszeilen exportiert.
- Der Export ist offline-first und enthält keine Cloud-Synchronisation.
- BLOB-Werte werden JSON-kompatibel als Base64-Struktur serialisiert.

## Struktur

```json
{
  "schema_version": "sqliteviewer-export-v1",
  "app_name": "SQLite Viewer Pro",
  "app_version": "2.0.0",
  "exported_at": "2026-05-25T11:34:56+02:00",
  "source": {
    "database_path": "C:/path/demo.sqlite",
    "database_name": "demo.sqlite",
    "view": "table",
    "table": "items",
    "query": null,
    "row_limit": 1000,
    "search_term": null,
    "sort_column": "id",
    "sort_descending": false
  },
  "columns": ["id", "name"],
  "row_count": 2,
  "result_rows": [
    {"id": 1, "name": "Alpha"},
    {"id": 2, "name": "Beta"}
  ]
}
```

## Feldbedeutung

- `schema_version`: Stabile Kennung des Exportvertrags.
- `app_name` / `app_version`: Herkunft des Exports.
- `exported_at`: ISO-8601-Zeitstempel mit Zeitzone.
- `source.database_path`: Ursprünglicher Datenbankpfad auf dem exportierenden System.
- `source.database_name`: Dateiname der Datenbank.
- `source.view`: Herkunft der sichtbaren Daten, aktuell `table`, `table_search` oder `query`.
- `source.table`: Aktive Tabelle, falls vorhanden.
- `source.query`: Ausgeführte SQL-Abfrage bei Query-Exporten.
- `source.row_limit`: Aktives Zeilenlimit der Ansicht.
- `source.search_term`: Aktiver Suchbegriff in der Tabellenansicht.
- `source.sort_column` / `source.sort_descending`: Sortierzustand der Tabellenansicht.
- `columns`: Sichtbare Spaltenreihenfolge.
- `row_count`: Anzahl exportierter Ergebniszeilen.
- `result_rows`: Ergebniszeilen als Objekte mit Spaltennamen.

## Wertkodierung

- `null`, `string`, `number` und `boolean` bleiben direkt erhalten.
- `bytes` werden als Objekt exportiert:

```json
{
  "type": "blob",
  "encoding": "base64",
  "size_bytes": 12,
  "data": "AAEC"
}
```

- Nicht direkt JSON-kompatible Sonderfälle werden als String serialisiert.

## Nicht-Ziele

- Kein vollständiger Dump interner SQLite-Metadaten.
- Kein bidirektionaler Importvertrag in v1.
- Keine Synchronisation kompletter Datenbanken zwischen Geräten.

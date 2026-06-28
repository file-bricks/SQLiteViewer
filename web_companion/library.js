export const SCHEMA = "sqliteviewer-export-v1";

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export function isBlobValue(value) {
  return isPlainObject(value)
    && value.type === "blob"
    && value.encoding === "base64"
    && typeof value.data === "string";
}

export function formatCellValue(value) {
  if (value === null || value === undefined) {
    return "";
  }

  if (isBlobValue(value)) {
    const printableSize = Number.isFinite(value.size_bytes) ? value.size_bytes : "?";
    return `BLOB (${printableSize} Bytes, Base64)`;
  }

  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

export function parseExport(payload) {
  if (!isPlainObject(payload)) {
    throw new Error("Export muss ein JSON-Objekt sein.");
  }

  if (payload.schema_version !== SCHEMA) {
    throw new Error(`Unbekanntes Schema: ${payload.schema_version ?? "leer"}`);
  }

  if (!Array.isArray(payload.columns)) {
    throw new Error("Export enthält keine gültige Spaltenliste.");
  }

  if (!Array.isArray(payload.result_rows)) {
    throw new Error("Export enthält keine gültigen Ergebniszeilen.");
  }

  const columns = payload.columns.map((column) => String(column));
  const source = isPlainObject(payload.source) ? payload.source : {};

  const rows = payload.result_rows.map((row, index) => {
    const rawRow = isPlainObject(row) ? row : {};
    const cells = columns.map((column) => rawRow[column] ?? null);
    const searchText = cells.map((value) => formatCellValue(value).toLowerCase()).join(" ");
    return {
      key: `${index}`,
      raw: rawRow,
      cells,
      searchText,
    };
  });

  return {
    raw: payload,
    schemaVersion: payload.schema_version,
    appName: typeof payload.app_name === "string" ? payload.app_name : "SQLite Viewer Pro",
    appVersion: typeof payload.app_version === "string" ? payload.app_version : "unbekannt",
    exportedAt: typeof payload.exported_at === "string" ? payload.exported_at : null,
    columns,
    rowCount: Number.isInteger(payload.row_count) ? payload.row_count : rows.length,
    rows,
    source: {
      databasePath: typeof source.database_path === "string" ? source.database_path : null,
      databaseName: typeof source.database_name === "string" ? source.database_name : null,
      view: typeof source.view === "string" ? source.view : "unknown",
      table: typeof source.table === "string" ? source.table : null,
      query: typeof source.query === "string" ? source.query : null,
      rowLimit: Number.isFinite(source.row_limit) ? source.row_limit : null,
      searchTerm: typeof source.search_term === "string" ? source.search_term : null,
      sortColumn: typeof source.sort_column === "string" ? source.sort_column : null,
      sortDescending: typeof source.sort_descending === "boolean" ? source.sort_descending : false,
    },
  };
}

export function filterRows(exportData, options = {}) {
  const query = String(options.query ?? "").trim().toLowerCase();
  if (!query) {
    return exportData.rows;
  }
  return exportData.rows.filter((row) => row.searchText.includes(query));
}

// Gibt einen RFC-4180-konformen CSV-String für die übergebenen Zeilen zurück.
// columns: string[] — Spaltenköpfe aus exportData.columns
// rows: ParsedRow[] — Zeilen aus parseExport().rows (ggf. bereits gefiltert)
export function exportToCsv(columns, rows) {
  function escapeCsvField(value) {
    const text = value === null || value === undefined ? "" : String(value);
    if (text.includes(",") || text.includes('"') || text.includes("\n") || text.includes("\r")) {
      return '"' + text.replace(/"/g, '""') + '"';
    }
    return text;
  }

  const header = columns.map(escapeCsvField).join(",");
  const dataLines = rows.map((row) =>
    row.cells.map((cell) => escapeCsvField(formatCellValue(cell))).join(",")
  );
  return [header, ...dataLines].join("\r\n");
}

// Sortiert die übergebenen Zeilen nach einer Spalte.
// rows: ParsedRow[] — Zeilen aus parseExport().rows (ggf. bereits gefiltert)
// columns: string[] — Spaltenköpfe aus exportData.columns (für Index-Lookup)
// options.sortKey: string | null — Spaltenname; null = unsortiert (Kopie der Eingabe)
// options.sortDescending: boolean — true = Z→A / groß→klein
export function sortRows(rows, columns, options = {}) {
  const { sortKey = null, sortDescending = false } = options;
  if (!sortKey) {
    return [...rows];
  }
  const colIndex = columns.indexOf(sortKey);
  if (colIndex === -1) {
    return [...rows];
  }
  return [...rows].sort((a, b) => {
    const aVal = a.cells[colIndex];
    const bVal = b.cells[colIndex];
    // null-Werte kommen unabhängig von der Sortierrichtung zuletzt
    if (aVal === null && bVal === null) return 0;
    if (aVal === null) return 1;
    if (bVal === null) return -1;
    // Beide Zahlen: numerischer Vergleich
    if (typeof aVal === "number" && typeof bVal === "number") {
      return sortDescending ? bVal - aVal : aVal - bVal;
    }
    // Blob-Werte: nach Byte-Größe vergleichen
    if (isBlobValue(aVal) && isBlobValue(bVal)) {
      const aSize = Number.isFinite(aVal.size_bytes) ? aVal.size_bytes : -1;
      const bSize = Number.isFinite(bVal.size_bytes) ? bVal.size_bytes : -1;
      return sortDescending ? bSize - aSize : aSize - bSize;
    }
    // Zeichenketten-Vergleich (Groß-/Kleinschreibung ignoriert)
    const aStr = formatCellValue(aVal).toLowerCase();
    const bStr = formatCellValue(bVal).toLowerCase();
    const cmp = aStr.localeCompare(bStr);
    return sortDescending ? -cmp : cmp;
  });
}

export function buildDemoExport() {
  return parseExport({
    schema_version: SCHEMA,
    app_name: "SQLite Viewer Pro",
    app_version: "2.0.0",
    exported_at: "2026-06-12T10:00:00+02:00",
    source: {
      database_path: "C:/demo/reading-list.sqlite",
      database_name: "reading-list.sqlite",
      view: "table_search",
      table: "books",
      query: null,
      row_limit: 250,
      search_term: "sqlite",
      sort_column: "rating",
      sort_descending: true
    },
    columns: ["id", "title", "rating", "cover_blob", "notes"],
    row_count: 3,
    result_rows: [
      {
        id: 1,
        title: "SQLite internals",
        rating: 5,
        cover_blob: {
          type: "blob",
          encoding: "base64",
          size_bytes: 12,
          data: "AAECAwQFBgc="
        },
        notes: "Demo-Zeile für Companion-Checks"
      },
      {
        id: 2,
        title: "Portable datasets",
        rating: 4,
        cover_blob: null,
        notes: "Zeigt lokale Export-Metadaten an"
      },
      {
        id: 3,
        title: "Offline review",
        rating: 4,
        cover_blob: null,
        notes: "Kein Cloud-Upload, keine Server-Pflicht"
      }
    ]
  });
}

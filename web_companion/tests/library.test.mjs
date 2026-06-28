import { test } from "node:test";
import assert from "node:assert/strict";

import { buildDemoExport, exportToCsv, filterRows, formatCellValue, parseExport, SCHEMA } from "../library.js";

const SAMPLE = {
  schema_version: SCHEMA,
  app_name: "SQLite Viewer Pro",
  app_version: "2.0.0",
  exported_at: "2026-06-12T10:00:00+02:00",
  source: {
    database_path: "C:/tmp/demo.sqlite",
    database_name: "demo.sqlite",
    view: "query",
    table: "items",
    query: "SELECT id, payload FROM items",
    row_limit: 100,
    search_term: "blob",
    sort_column: "id",
    sort_descending: false
  },
  columns: ["id", "payload", "title"],
  row_count: 2,
  result_rows: [
    {
      id: 1,
      payload: {
        type: "blob",
        encoding: "base64",
        size_bytes: 2,
        data: "QUI="
      },
      title: "Alpha"
    },
    {
      id: 2,
      payload: null,
      title: "Beta"
    }
  ]
};

test("parseExport maps metadata and rows", () => {
  const parsed = parseExport(SAMPLE);
  assert.equal(parsed.source.databaseName, "demo.sqlite");
  assert.equal(parsed.source.view, "query");
  assert.equal(parsed.columns.length, 3);
  assert.equal(parsed.rows.length, 2);
});

test("parseExport rejects unknown schema", () => {
  assert.throws(() => parseExport({ ...SAMPLE, schema_version: "other-v1" }), /Unbekanntes Schema/);
});

test("formatCellValue renders blob metadata readably", () => {
  const value = SAMPLE.result_rows[0].payload;
  assert.equal(formatCellValue(value), "BLOB (2 Bytes, Base64)");
});

test("filterRows searches across visible cell text", () => {
  const parsed = parseExport(SAMPLE);
  const rows = filterRows(parsed, { query: "beta" });
  assert.equal(rows.length, 1);
  assert.equal(rows[0].raw.title, "Beta");
});

test("parseExport keeps metadata as inert text for the UI renderer", () => {
  const parsed = parseExport({
    ...SAMPLE,
    source: {
      ...SAMPLE.source,
      database_name: "<img src=x onerror=alert(1)>"
    }
  });

  assert.equal(parsed.source.databaseName, "<img src=x onerror=alert(1)>");
});

test("buildDemoExport stays compatible with the schema", () => {
  const demo = buildDemoExport();
  assert.equal(demo.schemaVersion, SCHEMA);
  assert.ok(demo.rows.length >= 3);
  assert.equal(demo.source.view, "table_search");
});

test("formatCellValue falls back to ? when size_bytes is missing or non-finite", () => {
  // size_bytes undefined
  assert.equal(
    formatCellValue({ type: "blob", encoding: "base64", size_bytes: undefined, data: "AA==" }),
    "BLOB (? Bytes, Base64)"
  );
  // size_bytes NaN
  assert.equal(
    formatCellValue({ type: "blob", encoding: "base64", size_bytes: NaN, data: "AA==" }),
    "BLOB (? Bytes, Base64)"
  );
  // size_bytes valid number
  assert.equal(
    formatCellValue({ type: "blob", encoding: "base64", size_bytes: 42, data: "AA==" }),
    "BLOB (42 Bytes, Base64)"
  );
});

// --- exportToCsv ---

test("exportToCsv erzeugt Header und Datenzeilen mit CRLF-Trennung", () => {
  const parsed = parseExport(SAMPLE);
  const csv = exportToCsv(parsed.columns, parsed.rows);
  const lines = csv.split("\r\n");
  assert.equal(lines[0], "id,payload,title");
  assert.equal(lines.length, 3); // Header + 2 Datenzeilen
});

test("exportToCsv: Felder mit Komma werden in Anführungszeichen gesetzt", () => {
  const parsed = parseExport({
    ...SAMPLE,
    columns: ["note"],
    result_rows: [{ note: "links, rechts" }]
  });
  const csv = exportToCsv(parsed.columns, parsed.rows);
  assert.match(csv, /^note\r\n"links, rechts"$/);
});

test("exportToCsv: Anführungszeichen im Feld werden verdoppelt", () => {
  const parsed = parseExport({
    ...SAMPLE,
    columns: ["text"],
    result_rows: [{ text: 'Er sagte "Hallo"' }]
  });
  const csv = exportToCsv(parsed.columns, parsed.rows);
  assert.match(csv, /^text\r\n"Er sagte ""Hallo"""$/);
});

test("exportToCsv: null-Zellen ergeben leere Felder", () => {
  const parsed = parseExport(SAMPLE);
  // Zeile 2: payload ist null
  const csv = exportToCsv(parsed.columns, parsed.rows);
  const lines = csv.split("\r\n");
  // Zeile 2 (index 2): id=2, payload=null→"", title="Beta"
  assert.equal(lines[2], "2,,Beta");
});

test("exportToCsv: Blob-Werte werden als lesbarer Text exportiert", () => {
  const parsed = parseExport(SAMPLE);
  const csv = exportToCsv(parsed.columns, parsed.rows);
  const lines = csv.split("\r\n");
  // Zeile 1 (index 1): id=1, payload=BLOB..., title=Alpha
  // Feld enthält Komma → muss gequotet sein
  assert.match(lines[1], /^1,"BLOB \(2 Bytes, Base64\)",Alpha$/);
});

test("exportToCsv mit leerem Zeilenarray gibt nur den Header zurück", () => {
  const parsed = parseExport(SAMPLE);
  const csv = exportToCsv(parsed.columns, []);
  assert.equal(csv, "id,payload,title");
});

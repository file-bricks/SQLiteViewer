import { test } from "node:test";
import assert from "node:assert/strict";

import { buildDemoExport, filterRows, formatCellValue, parseExport, SCHEMA } from "../library.js";

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

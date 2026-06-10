"""Source-Platform Smoke-Test für SQLiteViewer.

Prüft auf Linux und macOS (und Windows) ohne GUI-Fenster:
- Modul-Import (tkinter muss installiert sein, aber kein DISPLAY nötig)
- Kernlogik über Fake-Infrastruktur
- SQLite-Ausführung headless
- Export-Serialisierung
"""
from __future__ import annotations

import base64
import sqlite3
from types import SimpleNamespace

import SQLiteViewer


def test_app_constants_defined():
    assert SQLiteViewer.APP_VERSION
    assert SQLiteViewer.APP_TITLE == "SQLite Viewer Pro"


def test_serialize_export_value_primitives():
    fake = SimpleNamespace()

    def serialize(v):
        return SQLiteViewer.SqlViewer._serialize_export_value(fake, v)

    assert serialize(None) is None
    assert serialize("hallo") == "hallo"
    assert serialize(42) == 42
    assert serialize(3.14) == 3.14
    assert serialize(True) is True


def test_serialize_export_value_bytes():
    fake = SimpleNamespace()

    def serialize(v):
        return SQLiteViewer.SqlViewer._serialize_export_value(fake, v)

    result = serialize(b"AB")
    assert result["type"] == "blob"
    assert result["encoding"] == "base64"
    assert result["size_bytes"] == 2
    assert base64.b64decode(result["data"]) == b"AB"


def test_build_export_payload_basic():
    fake = SimpleNamespace(
        current_columns=["id", "name"],
        current_data=[(1, "alpha")],
        db_path="/tmp/test.sqlite",
        export_context={
            "view": "table",
            "table": "items",
            "query": None,
            "row_limit": 100,
            "search_term": None,
            "sort_column": None,
            "sort_descending": False,
        },
    )
    fake._serialize_export_value = lambda v: SQLiteViewer.SqlViewer._serialize_export_value(fake, v)
    fake._build_export_payload = lambda: SQLiteViewer.SqlViewer._build_export_payload(fake)

    payload = fake._build_export_payload()

    assert payload["schema_version"] == "sqliteviewer-export-v1"
    assert payload["app_version"] == SQLiteViewer.APP_VERSION
    assert payload["columns"] == ["id", "name"]
    assert payload["row_count"] == 1
    assert payload["result_rows"] == [{"id": 1, "name": "alpha"}]
    assert payload["source"]["database_name"] == "test.sqlite"
    assert payload["source"]["view"] == "table"


def test_build_export_payload_bytes_row():
    fake = SimpleNamespace(
        current_columns=["blob_col"],
        current_data=[(b"\x00\xff",)],
        db_path="/tmp/blobs.sqlite",
        export_context={"view": "query", "table": "t", "query": "SELECT blob_col FROM t",
                        "row_limit": None, "search_term": None,
                        "sort_column": None, "sort_descending": None},
    )
    fake._serialize_export_value = lambda v: SQLiteViewer.SqlViewer._serialize_export_value(fake, v)
    fake._build_export_payload = lambda: SQLiteViewer.SqlViewer._build_export_payload(fake)

    payload = fake._build_export_payload()
    assert payload["result_rows"][0]["blob_col"]["type"] == "blob"
    assert payload["result_rows"][0]["blob_col"]["size_bytes"] == 2


def test_execute_sql_headless():
    """SQL-Ausführung über Fake-Infrastruktur ohne GUI."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items (name) VALUES ('smoke')")
    conn.commit()

    calls = {"populate": None}
    fake = SimpleNamespace(
        conn=conn,
        sql_text=SimpleNamespace(get=lambda *_: "SELECT name FROM items ORDER BY id"),
        sql_status=SimpleNamespace(config=lambda **_: None),
        table_var=SimpleNamespace(get=lambda: "items"),
        _populate_sql_result=lambda columns, rows: calls.__setitem__("populate", (columns, list(rows))),
        _clear_sql_result=lambda: None,
        _load_tables=lambda selected_table=None: None,
    )
    fake._set_current_view_data = lambda columns, rows: (
        setattr(fake, "current_columns", list(columns)),
        setattr(fake, "current_data", [tuple(row) for row in rows]),
    )
    fake._set_export_context = lambda **kwargs: setattr(fake, "export_context", kwargs)

    try:
        SQLiteViewer.SqlViewer.execute_sql(fake)
    finally:
        conn.close()

    assert calls["populate"] is not None
    columns, rows = calls["populate"]
    assert columns == ["name"]
    assert [row["name"] for row in rows] == ["smoke"]


def test_ident_escaping():
    fake = SimpleNamespace(_SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS)
    # Einfache Namen ohne Keyword-Konflikt bleiben unquotiert
    assert SQLiteViewer.SqlViewer._ident(fake, 'normal') == 'normal'
    # Namen mit Sonderzeichen oder SQLite-Keywords werden in doppelte Anführungszeichen gesetzt
    assert SQLiteViewer.SqlViewer._ident(fake, 'with"quote') == '"with""quote"'
    assert SQLiteViewer.SqlViewer._ident(fake, 'SELECT') == '"SELECT"'

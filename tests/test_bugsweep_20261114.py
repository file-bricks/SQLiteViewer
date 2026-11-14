"""Regressionstests — Bugsweep SQLiteViewer 2026-11-14."""
from __future__ import annotations

import SQLiteViewer
from test_execute_sql import _build_fake_viewer


def test_sql_tab_does_not_load_an_unbounded_result():
    """Die Tabellenansicht hält sich an ein Zeilenlimit, der SQL-Tab holte per fetchall() alles:
    „SELECT * FROM große_tabelle“ lud Millionen Zeilen in Speicher und Treeview — App friert ein."""
    fake, conn, status, calls = _build_fake_viewer("SELECT * FROM items")
    limit = SQLiteViewer.SQL_RESULT_MAX_ROWS
    conn.executemany("INSERT INTO items (name) VALUES (?)", [(f"n{i}",) for i in range(limit + 500)])
    conn.commit()
    try:
        SQLiteViewer.SqlViewer.execute_sql(fake)
    finally:
        conn.close()
    columns, rows = calls["populate"]
    assert len(rows) == limit
    assert str(limit) in status.get("text", "") and "+" in status.get("text", ""), status

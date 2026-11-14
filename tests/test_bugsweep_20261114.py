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


def test_table_search_ignores_case_of_umlauts():
    """SQLite-LIKE ignoriert Groß/Klein nur bei ASCII: „übersicht“ fand „Übersicht“ nicht, „ärzte“ nicht
    „Ärzte“ — im Deutschen stehen Ä/Ö/Ü oft am Wortanfang (gleiches Muster wie ProSync/DokuZen)."""
    from test_bugsweep_20260627 import _build_fake_for_search

    fake, conn, status, tree = _build_fake_for_search(["id", "name"], search_term="übersicht")
    conn.executemany("INSERT INTO items (name) VALUES (?)", [("Übersicht 2026",), ("Ärzte",), ("Notiz",)])
    conn.commit()
    try:
        SQLiteViewer.SqlViewer._search_data(fake)
        found = [row[1] for row in fake.current_data]
        fake.search_var.set("ärzte")
        SQLiteViewer.SqlViewer._search_data(fake)
        found_aerzte = [row[1] for row in fake.current_data]
        fake.search_var.set("50%")  # Wildcards bleiben maskiert
        SQLiteViewer.SqlViewer._search_data(fake)
        found_percent = fake.current_data
    finally:
        conn.close()
    assert "Suchfehler" not in status.get("text", ""), status
    assert found == ["Übersicht 2026"]
    assert found_aerzte == ["Ärzte"]
    assert found_percent == []


def test_search_export_context_keeps_the_typed_term():
    from test_bugsweep_20260627 import _build_fake_for_search

    fake, conn, status, tree = _build_fake_for_search(["id", "name"], search_term="Übersicht")
    try:
        SQLiteViewer.SqlViewer._search_data(fake)
    finally:
        conn.close()
    assert fake.export_context["search_term"] == "Übersicht"

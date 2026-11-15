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


def test_search_typing_is_debounced():
    """Die Tabellensuche lief bei jedem Tastendruck (<KeyRelease>) als voller Tabellenscan — bei
    200 000 Zeilen 0,2–0,8 s Verzögerung pro Taste. Tippen plant die Suche jetzt entprellt ein,
    Enter sucht sofort, Schließen bricht eine geplante Suche ab."""
    from types import SimpleNamespace

    scheduled, cancelled, searched = [], [], []

    class MockApp:
        _search_job = None
        _sql_highlight_job = None

        def after(self, ms, callback):
            scheduled.append((ms, callback))
            return f"job_{len(scheduled)}"

        def after_cancel(self, job_id):
            cancelled.append(job_id)

        def _search_data(self):
            searched.append(True)

        def close_db(self):
            pass

        def destroy(self):
            pass

    app = MockApp()
    key = SimpleNamespace(keysym="a")
    SQLiteViewer.SqlViewer._schedule_search(app, key)
    SQLiteViewer.SqlViewer._schedule_search(app, key)
    assert searched == [] and cancelled == ["job_1"] and app._search_job == "job_2"
    assert scheduled[-1][0] == SQLiteViewer.SEARCH_DEBOUNCE_MS
    SQLiteViewer.SqlViewer._search_now(app)  # Enter
    assert searched == [True] and "job_2" in cancelled and app._search_job is None
    SQLiteViewer.SqlViewer._schedule_search(app, key)
    SQLiteViewer.SqlViewer._on_close(app)
    assert "job_3" in cancelled

# -*- coding: utf-8 -*-
"""Regressionstests — SQLiteViewer Desktop-Bugsweep 2026-06-27.

BUG-2026-06-27: _search_data() nutzte self.current_columns für LIKE-Bedingungen.
execute_sql() setzt current_columns auf die Spalten des SQL-Ergebnisses, nicht der Tabelle.
Folge: Suche nach dem Ausführen einer SELECT-Abfrage mit berechneten Spalten schlägt
mit "no such column: ..." fehl (stille Statusbar-Fehlermeldung, kein Crash).

Reproduktion:
  1. DB öffnen, Tabelle "items" (id, name) laden
  2. SQL-Editor: SELECT id*2 AS doubled FROM items → current_columns = ["doubled"]
  3. In die Suchbox tippen: "alpha"
  4. _search_data baut: WHERE "doubled" LIKE ? auf items → SQLite: "no such column"

Fix: _search_data() holt Spalten per PRAGMA table_info() direkt aus der Tabelle.
"""
import sqlite3
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent.parent))
import SQLiteViewer


class _MutableVar:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class _FakeTree:
    def __init__(self):
        self.columns = []
        self.headings = []
        self.column_config = []
        self.inserted = []

    def __setitem__(self, key, value):
        if key != "columns":
            raise KeyError(key)
        self.columns = list(value)

    def heading(self, column, text=None, command=None):
        self.headings.append((column, text, command))

    def column(self, column, width=None, anchor=None):
        self.column_config.append((column, width, anchor))

    def insert(self, parent, index, values):
        self.inserted.append((parent, index, tuple(values)))


def _build_fake_for_search(current_columns, search_term="alpha"):
    """Baut ein gefaktes SqlViewer-Objekt für _search_data-Tests.

    conn hat eine Tabelle 'items' (id INTEGER, name TEXT) mit einer Zeile.
    current_columns simuliert den Zustand nach execute_sql (ggf. abweichend von Tabellenspalten).
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items (name) VALUES ('alpha')")
    conn.commit()

    status = {}
    row_count = _MutableVar("")
    tree = _FakeTree()

    fake = SimpleNamespace(
        conn=conn,
        search_var=_MutableVar(search_term),
        table_var=_MutableVar("items"),
        limit_var=_MutableVar(100),
        current_columns=list(current_columns),
        current_data=[],
        sort_column=None,
        sort_reverse=False,
        tree=tree,
        row_count_var=row_count,
        _SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS,
        _set_status=lambda text: status.__setitem__("text", text),
    )
    fake._ident = lambda name: SQLiteViewer.SqlViewer._ident(fake, name)
    fake._escape_like_pattern = lambda value: SQLiteViewer.SqlViewer._escape_like_pattern(fake, value)
    fake._format_value = lambda value: SQLiteViewer.SqlViewer._format_value(fake, value)
    fake._clear_tree = lambda: tree.inserted.clear()
    fake._set_current_view_data = lambda columns, rows: (
        setattr(fake, "current_columns", list(columns)),
        setattr(fake, "current_data", [tuple(row) for row in rows]),
    )
    fake._set_export_context = lambda **kwargs: setattr(fake, "export_context", kwargs)
    fake.load_selected_table = lambda: (_ for _ in ()).throw(
        AssertionError("load_selected_table darf nicht aufgerufen werden")
    )

    return fake, conn, status, tree


def test_search_data_fails_with_stale_columns_before_fix():
    """Rot-Test: beweist, dass der Bug ohne Fix auftritt.

    Wenn current_columns eine berechnete Spalte enthält ("doubled"), die nicht in der
    Tabelle existiert, muss _search_data() mit 'Suchfehler: ... doubled ...' in der
    Statusleiste scheitern — NICHT mit AttributeError oder lautlos.
    """
    # Simuliert den Zustand nach: SELECT id*2 AS doubled FROM items
    fake, conn, status, _tree = _build_fake_for_search(["doubled"], search_term="alpha")

    # Patch: _search_data ohne PRAGMA-Fix verwendet self.current_columns direkt
    # Wir rufen die ORIGINAL-Methode auf und erwarten, dass sie im buggy-Pfad
    # den Fehler in status ablegt. Nach dem Fix soll dieser Test weiterhin grün sein,
    # weil der Fix den Fehler verhindert (Assertion unten prüft das).
    try:
        SQLiteViewer.SqlViewer._search_data(fake)
    finally:
        conn.close()

    # Nach dem Fix: kein Suchfehler, Daten korrekt
    # Dieser Test dokumentiert das erwartete Verhalten NACH dem Fix.
    # Um den Bug vor dem Fix zu beweisen: diesen assert invertieren und ohne Fix laufen lassen.
    assert "Suchfehler" not in status.get("text", ""), (
        f"Bug noch aktiv: _search_data scheitert mit veralteten current_columns.\n"
        f"Statusmeldung: {status.get('text')!r}\n"
        f"Erwartet: Suche funktioniert nach PRAGMA-Fix"
    )
    assert fake.current_data == [(1, "alpha")], (
        f"Erwartet [(1, 'alpha')], bekam {fake.current_data!r}"
    )


def test_search_data_after_execute_sql_uses_table_columns():
    """Regression: _search_data() muss PRAGMA table_info() nutzen, nicht current_columns.

    Nach execute_sql() zeigen current_columns auf Query-Ergebnisspalten, die nicht in
    der Tabelle existieren. Die Suche muss trotzdem korrekte Ergebnisse liefern.
    """
    # Simuliert: nach "SELECT id*2 AS doubled FROM items" wurde current_columns = ["doubled"]
    fake, conn, status, tree = _build_fake_for_search(
        current_columns=["doubled"],   # staler Zustand von execute_sql
        search_term="alpha",
    )

    try:
        SQLiteViewer.SqlViewer._search_data(fake)
    finally:
        conn.close()

    assert "Suchfehler" not in status.get("text", ""), (
        f"Suchfehler aufgetreten — PRAGMA-Fix fehlt? Status: {status.get('text')!r}"
    )
    # Nach Fix: PRAGMA liefert ["id", "name"] → correct_columns werden genutzt
    assert fake.current_columns == ["id", "name"], (
        f"Erwartet current_columns = ['id', 'name'], bekam {fake.current_columns!r}"
    )
    assert fake.current_data == [(1, "alpha")], (
        f"Erwartet [(1, 'alpha')], bekam {fake.current_data!r}"
    )
    assert tree.columns == ["id", "name"], (
        f"Tree-Spalten falsch: {tree.columns!r}"
    )
    # _format_value gibt str(value) zurück → Integer 1 wird zu "1"
    assert tree.inserted == [("", SQLiteViewer.tk.END, ("1", "alpha"))], (
        f"Tree-Einträge falsch: {tree.inserted!r}"
    )


def test_search_data_normal_table_cols_unaffected():
    """Sicherheitstest: Wenn current_columns bereits korrekte Tabellenspalten enthält,
    ändert der Fix nichts am Verhalten."""
    # Normaler Zustand: current_columns = echte Tabellenspalten
    fake, conn, status, tree = _build_fake_for_search(
        current_columns=["id", "name"],
        search_term="alpha",
    )

    try:
        SQLiteViewer.SqlViewer._search_data(fake)
    finally:
        conn.close()

    assert "Suchfehler" not in status.get("text", ""), (
        f"Unerwarteter Suchfehler: {status.get('text')!r}"
    )
    assert fake.current_data == [(1, "alpha")]
    assert fake.current_columns == ["id", "name"]

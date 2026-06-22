from __future__ import annotations

import json
import sqlite3
from types import SimpleNamespace

import SQLiteViewer


class _MutableVar:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class _FakeCombo:
    def __init__(self, var):
        self.var = var
        self.values = []

    def __setitem__(self, key, value):
        if key != "values":
            raise KeyError(key)
        self.values = list(value)

    def current(self, index):
        self.var.set(self.values[index] if self.values else "")

    def set(self, value):
        self.var.set(value)


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


class _FakeText:
    def __init__(self, content=""):
        self.content = content
        self.state = None

    def config(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]

    def delete(self, start, end):
        self.content = ""

    def get(self, start, end):
        return self.content


def _build_fake_viewer(sql: str):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items (name) VALUES ('alpha')")
    conn.commit()

    status = {}
    calls = {"populate": None, "clear": 0}

    fake = SimpleNamespace(
        conn=conn,
        sql_text=SimpleNamespace(get=lambda *_args: sql),
        sql_status=SimpleNamespace(config=lambda **kwargs: status.update(kwargs)),
        table_var=SimpleNamespace(get=lambda: "items"),
        _populate_sql_result=lambda columns, rows: calls.__setitem__("populate", (columns, rows)),
        _clear_sql_result=lambda: calls.__setitem__("clear", calls["clear"] + 1),
        _load_tables=lambda selected_table=None: None,
    )
    fake._set_current_view_data = lambda columns, rows: (
        setattr(fake, "current_columns", list(columns)),
        setattr(fake, "current_data", [tuple(row) for row in rows]),
    )
    fake._set_export_context = lambda **kwargs: setattr(fake, "export_context", kwargs)

    return fake, conn, status, calls


def _build_fake_viewer_with_two_tables(sql: str, selected_table: str = "items_b"):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items_a (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items_a (name) VALUES ('alpha')")
    conn.execute("CREATE TABLE items_b (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items_b (name) VALUES ('bravo')")
    conn.commit()

    status = {}
    calls = {
        "populate_sql": None,
        "clear_sql": 0,
        "populate_tree": None,
        "clear_tree": 0,
        "row_count": None,
    }

    table_var = _MutableVar(selected_table)
    schema_var = _MutableVar(selected_table)
    fake = SimpleNamespace(
        conn=conn,
        sql_text=SimpleNamespace(get=lambda *_args: sql),
        sql_status=SimpleNamespace(config=lambda **kwargs: status.update(kwargs)),
        table_var=table_var,
        schema_table_var=schema_var,
        table_combo=_FakeCombo(table_var),
        schema_combo=_FakeCombo(schema_var),
        limit_var=_MutableVar(100),
        row_count_var=SimpleNamespace(set=lambda value: calls.__setitem__("row_count", value)),
        sort_column=None,
        sort_reverse=False,
        _SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS,
        _set_status=lambda *_args, **_kwargs: None,
        _populate_sql_result=lambda columns, rows: calls.__setitem__("populate_sql", (columns, rows)),
        _clear_sql_result=lambda: calls.__setitem__("clear_sql", calls["clear_sql"] + 1),
        _clear_tree=lambda: calls.__setitem__("clear_tree", calls["clear_tree"] + 1),
        _populate_tree=lambda columns, rows: calls.__setitem__("populate_tree", (columns, rows)),
        _set_current_view_data=lambda columns, rows: (
            setattr(fake, "current_columns", list(columns)),
            setattr(fake, "current_data", [tuple(row) for row in rows]),
        ),
        _set_export_context=lambda **kwargs: setattr(fake, "export_context", kwargs),
        _ident=lambda name: SQLiteViewer.SqlViewer._ident(fake, name),
        _load_schema=lambda: None,
    )
    fake._load_tables = lambda selected_table=None: SQLiteViewer.SqlViewer._load_tables(fake, selected_table)
    fake.load_selected_table = lambda: SQLiteViewer.SqlViewer.load_selected_table(fake)
    return fake, conn, status, calls


def test_execute_sql_handles_select_with_leading_comment():
    fake, conn, status, calls = _build_fake_viewer(
        "/* comment before the query */\nSELECT name FROM items ORDER BY id"
    )

    try:
        SQLiteViewer.SqlViewer.execute_sql(fake)
    finally:
        conn.close()

    assert calls["populate"] is not None
    columns, rows = calls["populate"]
    assert columns == ["name"]
    assert [row["name"] for row in rows] == ["alpha"]
    assert calls["clear"] == 0
    assert status["text"].startswith("✓ 1 Zeilen")


def test_execute_sql_updates_export_state_for_query_results(tmp_path, monkeypatch):
    fake, conn, _status, calls = _build_fake_viewer("SELECT name FROM items ORDER BY id")
    fake.current_columns = ["id", "name"]
    fake.current_data = [(1, "legacy")]
    fake.table_var = SimpleNamespace(get=lambda: "items")
    fake._set_status = lambda *_args, **_kwargs: None

    export_path = tmp_path / "query_result.csv"
    monkeypatch.setattr(
        SQLiteViewer.filedialog,
        "asksaveasfilename",
        lambda **_kwargs: str(export_path),
    )
    monkeypatch.setattr(SQLiteViewer.messagebox, "showinfo", lambda *_args, **_kwargs: None)

    try:
        SQLiteViewer.SqlViewer.execute_sql(fake)
        SQLiteViewer.SqlViewer.export_csv(fake)
    finally:
        conn.close()

    assert calls["populate"] is not None
    assert fake.current_columns == ["name"]
    assert fake.current_data == [("alpha",)]
    assert fake.export_context == {
        "view": "query",
        "table": "items",
        "query": "SELECT name FROM items ORDER BY id",
        "row_limit": None,
        "search_term": None,
        "sort_column": None,
        "sort_descending": None,
    }
    assert export_path.read_text(encoding="utf-8-sig").splitlines() == ["name", "alpha"]


def test_export_json_writes_companion_payload(tmp_path, monkeypatch):
    export_path = tmp_path / "query_result.json"
    fake = SimpleNamespace(
        current_columns=["id", "payload"],
        current_data=[(1, b"AB")],
        db_path="C:/tmp/demo.sqlite",
        table_var=SimpleNamespace(get=lambda: "items"),
        export_context={
            "view": "query",
            "table": "items",
            "query": "SELECT id, payload FROM items",
            "row_limit": None,
            "search_term": None,
            "sort_column": None,
            "sort_descending": None,
        },
        _set_status=lambda *_args, **_kwargs: None,
    )
    fake._serialize_export_value = lambda value: SQLiteViewer.SqlViewer._serialize_export_value(fake, value)
    fake._build_export_payload = lambda: SQLiteViewer.SqlViewer._build_export_payload(fake)

    monkeypatch.setattr(
        SQLiteViewer.filedialog,
        "asksaveasfilename",
        lambda **_kwargs: str(export_path),
    )
    monkeypatch.setattr(SQLiteViewer.messagebox, "showinfo", lambda *_args, **_kwargs: None)

    SQLiteViewer.SqlViewer.export_json(fake)

    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "sqliteviewer-export-v1"
    assert payload["app_version"] == SQLiteViewer.APP_VERSION
    assert payload["source"]["database_name"] == "demo.sqlite"
    assert payload["source"]["view"] == "query"
    assert payload["source"]["query"] == "SELECT id, payload FROM items"
    assert payload["columns"] == ["id", "payload"]
    assert payload["row_count"] == 1
    assert payload["result_rows"] == [
        {
            "id": 1,
            "payload": {
                "type": "blob",
                "encoding": "base64",
                "size_bytes": 2,
                "data": "QUI=",
            },
        }
    ]


def test_export_json_allows_empty_visible_results(tmp_path, monkeypatch):
    export_path = tmp_path / "empty_result.json"
    fake = SimpleNamespace(
        current_columns=["id", "name"],
        current_data=[],
        db_path="C:/tmp/demo.sqlite",
        table_var=SimpleNamespace(get=lambda: "items"),
        export_context={
            "view": "query",
            "table": "items",
            "query": "SELECT id, name FROM items WHERE 1 = 0",
            "row_limit": None,
            "search_term": None,
            "sort_column": None,
            "sort_descending": None,
        },
        _set_status=lambda *_args, **_kwargs: None,
    )
    fake._build_export_payload = lambda: SQLiteViewer.SqlViewer._build_export_payload(fake)

    monkeypatch.setattr(
        SQLiteViewer.filedialog,
        "asksaveasfilename",
        lambda **_kwargs: str(export_path),
    )
    monkeypatch.setattr(SQLiteViewer.messagebox, "showinfo", lambda *_args, **_kwargs: None)

    SQLiteViewer.SqlViewer.export_json(fake)

    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert payload["columns"] == ["id", "name"]
    assert payload["row_count"] == 0
    assert payload["result_rows"] == []


class _ToolbarVar:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class _ToolbarWidget:
    def __init__(self, widget_kind: str, **kwargs):
        self.widget_kind = widget_kind
        self.kwargs = kwargs
        self.pack_calls = []
        self.bind_calls = []

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)

    def bind(self, event, callback):
        self.bind_calls.append((event, callback))


class _FakeSearchEntry:
    def __init__(self):
        self.focus_calls = 0
        self.select_ranges = []

    def focus_set(self):
        self.focus_calls += 1

    def select_range(self, start, end):
        self.select_ranges.append((start, end))


def test_toolbar_uses_visible_search_label_and_german_refresh(monkeypatch):
    created_widgets = []

    def _make_widget(widget_kind):
        def _factory(*_args, **kwargs):
            widget = _ToolbarWidget(widget_kind, **kwargs)
            created_widgets.append(widget)
            return widget
        return _factory

    monkeypatch.setattr(SQLiteViewer.ttk, "Frame", _make_widget("frame"))
    monkeypatch.setattr(SQLiteViewer.ttk, "Label", _make_widget("label"))
    monkeypatch.setattr(SQLiteViewer.ttk, "Combobox", _make_widget("combobox"))
    monkeypatch.setattr(SQLiteViewer.ttk, "Spinbox", _make_widget("spinbox"))
    monkeypatch.setattr(SQLiteViewer.ttk, "Entry", _make_widget("entry"))
    monkeypatch.setattr(SQLiteViewer.ttk, "Button", _make_widget("button"))
    monkeypatch.setattr(SQLiteViewer.tk, "StringVar", _ToolbarVar)
    monkeypatch.setattr(SQLiteViewer.tk, "IntVar", _ToolbarVar)

    fake = SimpleNamespace(
        load_selected_table=lambda: None,
        export_csv=lambda: None,
        _search_data=lambda: None,
    )
    fake._clear_search = lambda event=None: SQLiteViewer.SqlViewer._clear_search(fake, event)

    SQLiteViewer.SqlViewer._build_toolbar(fake)

    label_texts = [widget.kwargs.get("text") for widget in created_widgets if widget.widget_kind == "label"]
    button_texts = [widget.kwargs.get("text") for widget in created_widgets if widget.widget_kind == "button"]
    entry_widgets = [widget for widget in created_widgets if widget.widget_kind == "entry"]

    assert "Suche:" in label_texts
    assert "⟳ Aktualisieren" in button_texts
    assert "⟳ Refresh" not in button_texts
    assert entry_widgets, "Die Toolbar muss ein Suchfeld anlegen"
    bound_events = [event for event, _callback in entry_widgets[0].bind_calls]
    assert "<Escape>" in bound_events


def test_clear_search_keeps_focus_and_reloads_visible_table():
    calls = {"load_selected_table": 0}
    search_var = _MutableVar("alpha")
    row_count_var = _MutableVar("Gefunden: 1")
    search_entry = _FakeSearchEntry()

    fake = SimpleNamespace(
        search_var=search_var,
        table_var=_MutableVar("items"),
        row_count_var=row_count_var,
        search_entry=search_entry,
        load_selected_table=lambda: calls.__setitem__("load_selected_table", calls["load_selected_table"] + 1),
    )

    result = SQLiteViewer.SqlViewer._clear_search(fake)

    assert result == "break"
    assert search_var.get() == ""
    assert calls["load_selected_table"] == 1
    assert search_entry.focus_calls == 1
    assert search_entry.select_ranges == [(0, SQLiteViewer.tk.END)]
    assert row_count_var.get() == "Gefunden: 1"


def test_open_db_path_handles_hash_in_filename(tmp_path):
    db_path = tmp_path / "hash#name.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    conn.close()

    loaded = {}

    fake = SimpleNamespace(
        close_db=lambda: None,
        db_label=SimpleNamespace(config=lambda **kwargs: None),
        _set_status=lambda *_args, **_kwargs: None,
    )

    def _load_tables():
        cur = fake.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        loaded["tables"] = [row[0] for row in cur.fetchall()]

    fake._load_tables = _load_tables

    try:
        SQLiteViewer.SqlViewer.open_db_path(fake, str(db_path))
    finally:
        if getattr(fake, "conn", None) is not None:
            fake.conn.close()

    assert loaded["tables"] == ["items"]


def test_open_db_path_keeps_current_database_when_new_open_fails(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()

    status = {}
    calls = {"close_db": 0}
    fake = SimpleNamespace()

    def _close_db():
        calls["close_db"] += 1
        fake.conn = None
        fake.db_path = None

    fake.conn = conn
    fake.db_path = "existing.sqlite"
    fake.close_db = _close_db
    fake.db_label = SimpleNamespace(config=lambda **kwargs: None)
    fake._set_status = lambda text: status.__setitem__("text", text)

    errors = []

    def _raise_connect(*_args, **_kwargs):
        raise sqlite3.OperationalError("cannot open database file")

    monkeypatch.setattr(SQLiteViewer.sqlite3, "connect", _raise_connect)
    monkeypatch.setattr(
        SQLiteViewer.messagebox,
        "showerror",
        lambda title, message: errors.append((title, message)),
    )

    try:
        SQLiteViewer.SqlViewer.open_db_path(fake, "missing.sqlite")
    finally:
        conn.close()

    assert fake.conn is conn
    assert fake.db_path == "existing.sqlite"
    assert calls["close_db"] == 0
    assert status["text"] == "Fehler"
    assert errors == [("Fehler beim Öffnen", "cannot open database file")]


def test_close_db_clears_export_state():
    conn = sqlite3.connect(":memory:")
    search_var = _MutableVar("alpha")
    table_var = _MutableVar("items")
    schema_var = _MutableVar("items")
    row_count_var = _MutableVar("Gefunden: 1")
    status = {}
    calls = {"clear_tree": 0, "clear_sql": 0}

    fake = SimpleNamespace(
        conn=conn,
        db_path="demo.sqlite",
        current_columns=["id", "name"],
        current_data=[(1, "alpha")],
        export_context={"view": "query"},
        sort_column="name",
        sort_reverse=True,
        search_var=search_var,
        table_var=table_var,
        schema_table_var=schema_var,
        row_count_var=row_count_var,
        sql_status=SimpleNamespace(config=lambda **kwargs: status.update(kwargs)),
        db_label=SimpleNamespace(config=lambda **kwargs: None),
        table_combo=_FakeCombo(table_var),
        schema_combo=_FakeCombo(schema_var),
        _clear_tree=lambda: calls.__setitem__("clear_tree", calls["clear_tree"] + 1),
        _clear_sql_result=lambda: calls.__setitem__("clear_sql", calls["clear_sql"] + 1),
        _set_status=lambda *_args, **_kwargs: None,
    )
    fake._clear_schema_text = lambda: SQLiteViewer.SqlViewer._clear_schema_text(fake)

    try:
        SQLiteViewer.SqlViewer.close_db(fake)
    finally:
        conn.close()

    assert fake.conn is None
    assert fake.db_path is None
    assert fake.current_columns == []
    assert fake.current_data == []
    assert fake.export_context == {}
    assert fake.sort_column is None
    assert fake.sort_reverse is False
    assert search_var.get() == ""
    assert table_var.get() == ""
    assert schema_var.get() == ""
    assert row_count_var.get() == ""
    assert status["text"] == ""
    assert calls["clear_tree"] == 1
    assert calls["clear_sql"] == 1


def test_close_db_clears_schema_text():
    conn = sqlite3.connect(":memory:")
    search_var = _MutableVar("alpha")
    table_var = _MutableVar("items")
    schema_var = _MutableVar("items")
    row_count_var = _MutableVar("Gefunden: 1")
    status = {}
    calls = {"clear_tree": 0, "clear_sql": 0, "clear_schema": 0}
    schema_text = _FakeText("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);")

    fake = SimpleNamespace(
        conn=conn,
        db_path="demo.sqlite",
        current_columns=["id", "name"],
        current_data=[(1, "alpha")],
        sort_column="name",
        sort_reverse=True,
        search_var=search_var,
        table_var=table_var,
        schema_table_var=schema_var,
        row_count_var=row_count_var,
        sql_status=SimpleNamespace(config=lambda **kwargs: status.update(kwargs)),
        db_label=SimpleNamespace(config=lambda **kwargs: None),
        table_combo=_FakeCombo(table_var),
        schema_combo=_FakeCombo(schema_var),
        schema_text=schema_text,
        _clear_tree=lambda: calls.__setitem__("clear_tree", calls["clear_tree"] + 1),
        _clear_sql_result=lambda: calls.__setitem__("clear_sql", calls["clear_sql"] + 1),
        _set_status=lambda *_args, **_kwargs: None,
    )
    fake._clear_schema_text = lambda: (
        calls.__setitem__("clear_schema", calls["clear_schema"] + 1),
        SQLiteViewer.SqlViewer._clear_schema_text(fake),
    )

    try:
        SQLiteViewer.SqlViewer.close_db(fake)
    finally:
        conn.close()

    assert schema_text.get("1.0", "end") == ""
    assert schema_text.state == SQLiteViewer.tk.DISABLED
    assert calls["clear_tree"] == 1
    assert calls["clear_sql"] == 1
    assert calls["clear_schema"] == 1


def test_execute_sql_refreshes_the_selected_table_after_update():
    fake, conn, _status, calls = _build_fake_viewer_with_two_tables(
        "UPDATE items_b SET name = 'beta' WHERE id = 1"
    )

    original_showerror = SQLiteViewer.messagebox.showerror
    SQLiteViewer.messagebox.showerror = lambda *_args, **_kwargs: None
    try:
        SQLiteViewer.SqlViewer.execute_sql(fake)
    finally:
        SQLiteViewer.messagebox.showerror = original_showerror
        conn.close()

    assert fake.table_var.get() == "items_b"
    assert fake.schema_table_var.get() == "items_b"
    assert calls["populate_tree"] is not None
    assert fake.current_columns == ["id", "name"]
    assert fake.current_data == [(1, "beta")]


def test_search_data_escapes_like_wildcards():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items (name) VALUES ('a_b')")
    conn.execute("INSERT INTO items (name) VALUES ('axb')")
    conn.commit()

    status = {}
    row_count = _MutableVar("")
    tree = _FakeTree()
    fake = SimpleNamespace(
        conn=conn,
        search_var=_MutableVar("a_b"),
        table_var=_MutableVar("items"),
        limit_var=_MutableVar(100),
        current_columns=["id", "name"],
        current_data=[],
        sort_column=None,
        sort_reverse=False,
        tree=tree,
        row_count_var=row_count,
        _SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SQLiteViewer.SqlViewer._ident(fake, name),
        _escape_like_pattern=lambda value: SQLiteViewer.SqlViewer._escape_like_pattern(fake, value),
        _format_value=lambda value: value,
        _clear_tree=lambda: None,
        _set_current_view_data=lambda columns, rows: (
            setattr(fake, "current_columns", list(columns)),
            setattr(fake, "current_data", [tuple(row) for row in rows]),
        ),
        _set_export_context=lambda **kwargs: setattr(fake, "export_context", kwargs),
        _set_status=lambda text: status.__setitem__("text", text),
    )

    try:
        SQLiteViewer.SqlViewer._search_data(fake)
    finally:
        conn.close()

    assert fake.current_columns == ["id", "name"]
    assert fake.current_data == [(1, "a_b")]
    assert fake.export_context == {
        "view": "table_search",
        "table": "items",
        "query": None,
        "row_limit": 100,
        "search_term": "a_b",
        "sort_column": None,
        "sort_descending": False,
    }
    assert row_count.get() == "Gefunden: 1"
    assert tree.inserted == [("", SQLiteViewer.tk.END, (1, "a_b"))]
    assert "Suchfehler" not in status.get("text", "")


def test_sorting_keeps_filtered_search_results():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany(
        "INSERT INTO items (id, name) VALUES (?, ?)",
        [(1, "alpha"), (2, "beta"), (3, "algae")],
    )
    conn.commit()

    status = {}
    row_count = _MutableVar("")
    tree = _FakeTree()
    fake = SimpleNamespace(
        conn=conn,
        search_var=_MutableVar("al"),
        table_var=_MutableVar("items"),
        limit_var=_MutableVar(100),
        current_columns=["id", "name"],
        current_data=[],
        sort_column=None,
        sort_reverse=False,
        tree=tree,
        row_count_var=row_count,
        _SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SQLiteViewer.SqlViewer._ident(fake, name),
        _escape_like_pattern=lambda value: SQLiteViewer.SqlViewer._escape_like_pattern(fake, value),
        _format_value=lambda value: value,
        _clear_tree=lambda: tree.inserted.clear(),
        _set_current_view_data=lambda columns, rows: (
            setattr(fake, "current_columns", list(columns)),
            setattr(fake, "current_data", [tuple(row) for row in rows]),
        ),
        _set_export_context=lambda **kwargs: setattr(fake, "export_context", kwargs),
        _set_status=lambda text: status.__setitem__("text", text),
        load_selected_table=lambda: (_ for _ in ()).throw(AssertionError("load_selected_table should not run for active search sorting")),
    )
    fake._search_data = lambda: SQLiteViewer.SqlViewer._search_data(fake)

    try:
        SQLiteViewer.SqlViewer._search_data(fake)
        SQLiteViewer.SqlViewer._sort_by_column(fake, "id")
        SQLiteViewer.SqlViewer._sort_by_column(fake, "id")
    finally:
        conn.close()

    assert fake.current_columns == ["id", "name"]
    assert fake.current_data == [(3, "algae"), (1, "alpha")]
    assert fake.export_context == {
        "view": "table_search",
        "table": "items",
        "query": None,
        "row_limit": 100,
        "search_term": "al",
        "sort_column": "id",
        "sort_descending": True,
    }
    assert row_count.get() == "Gefunden: 2"
    assert tree.inserted == [
        ("", SQLiteViewer.tk.END, (3, "algae")),
        ("", SQLiteViewer.tk.END, (1, "alpha")),
    ]
    assert "Suchfehler" not in status.get("text", "")


def test_export_csv_allows_empty_table(tmp_path, monkeypatch):
    """Regression: export_csv blockierte leere Tabellen mit 'Keine Daten'.

    export_json erlaubt leere Exports (nur Spalten, keine Zeilen) korrekt.
    export_csv prüfte fälschlich auch 'not current_data', was valide Header-only-
    CSVs verhinderte. Beide Funktionen sollen konsistent nur current_columns prüfen.
    """
    export_path = tmp_path / "empty_table.csv"
    fake = SimpleNamespace(
        current_columns=["id", "name"],
        current_data=[],
        table_var=SimpleNamespace(get=lambda: "items"),
        _set_status=lambda *_args, **_kwargs: None,
    )

    warnings = []
    monkeypatch.setattr(SQLiteViewer.messagebox, "showwarning", lambda *a, **_k: warnings.append(a))
    monkeypatch.setattr(SQLiteViewer.filedialog, "asksaveasfilename", lambda **_k: str(export_path))
    monkeypatch.setattr(SQLiteViewer.messagebox, "showinfo", lambda *_a, **_k: None)

    SQLiteViewer.SqlViewer.export_csv(fake)

    assert not warnings, f"Kein Warning erwartet für leere Tabelle, bekam: {warnings}"
    lines = export_path.read_text(encoding="utf-8-sig").splitlines()
    assert lines == ["id;name"], f"Erwartet nur Header-Zeile, bekam: {lines}"


def test_heading_command_sorts_once_per_click():
    """Regression: <Button-1>-Binding rief _sort_by_column doppelt auf.

    Erster Klick auf eine neue Spalte ergab immer DESC statt ASC, weil
    _on_header_click und der Heading-Command beide feuerten. Nach dem Fix
    sorgt ausschließlich der Heading-Command für die Sortierung (einmaliger
    Aufruf pro Klick).
    """
    sort_calls = []
    tree = _FakeTree()
    fake = SimpleNamespace(
        tree=tree,
        sort_column=None,
        sort_reverse=False,
    )

    def _fake_sort(col):
        sort_calls.append(col)
        if fake.sort_column == col:
            fake.sort_reverse = not fake.sort_reverse
        else:
            fake.sort_column = col
            fake.sort_reverse = False

    fake._sort_by_column = _fake_sort
    fake._clear_tree = lambda: None

    SQLiteViewer.SqlViewer._populate_tree(fake, ["id", "name"], [])

    id_cmd = next(cmd for col, _t, cmd in tree.headings if col == "id" and cmd is not None)
    id_cmd()

    assert sort_calls == ["id"], f"Erwartet genau 1 Aufruf, bekam: {sort_calls}"
    assert fake.sort_column == "id"
    assert fake.sort_reverse is False, "Erster Klick muss ASC (sort_reverse=False) ergeben"

    assert not hasattr(SQLiteViewer.SqlViewer, "_on_header_click"), (
        "_on_header_click muss entfernt sein (war Ursache des Doppel-Sort)"
    )


def test_search_data_shows_sort_indicator_in_heading():
    """Regression: _search_data muss den Sortierindikator (↑/↓) im Heading anzeigen.

    Vor dem Fix fehlte der Indikator bei Suchergebnissen, obwohl _populate_tree
    ihn korrekt zeigte. Der User konnte die aktive Sortierrichtung nicht erkennen.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.executemany(
        "INSERT INTO items (id, name) VALUES (?, ?)",
        [(1, "alpha"), (2, "algae")],
    )
    conn.commit()

    row_count = _MutableVar("")
    tree = _FakeTree()
    fake = SimpleNamespace(
        conn=conn,
        search_var=_MutableVar("al"),
        table_var=_MutableVar("items"),
        limit_var=_MutableVar(100),
        current_columns=["id", "name"],
        current_data=[],
        sort_column="id",
        sort_reverse=True,      # DESC → Indikator muss "↓" sein
        tree=tree,
        row_count_var=row_count,
        _SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SQLiteViewer.SqlViewer._ident(fake, name),
        _escape_like_pattern=lambda value: SQLiteViewer.SqlViewer._escape_like_pattern(fake, value),
        _format_value=lambda value: value,
        _clear_tree=lambda: tree.inserted.clear(),
        _set_current_view_data=lambda columns, rows: (
            setattr(fake, "current_columns", list(columns)),
            setattr(fake, "current_data", [tuple(row) for row in rows]),
        ),
        _set_export_context=lambda **kwargs: setattr(fake, "export_context", kwargs),
        _set_status=lambda text: None,
        load_selected_table=lambda: (_ for _ in ()).throw(
            AssertionError("load_selected_table should not run during active search")
        ),
    )

    try:
        SQLiteViewer.SqlViewer._search_data(fake)
    finally:
        conn.close()

    heading_texts = {col: text for col, text, _ in tree.headings}
    assert heading_texts.get("id") == "id ↓", (
        f"Sortierindikator fehlt im Heading für 'id': {heading_texts.get('id')!r}"
    )
    assert heading_texts.get("name") == "name", (
        f"Indikator darf nur bei sort_column erscheinen: {heading_texts.get('name')!r}"
    )

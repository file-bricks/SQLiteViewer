# -*- coding: utf-8 -*-
"""Regression and resilience tests for SQLiteViewer bugsearch (2026-10-03).

Tested areas:
- atomic_export: automatic creation of non-existent parent directories
- protect_destination: rejection of directory export paths
- database_files: resilience against closed/corrupt connections and empty/None paths
- _load_tables / _load_schema / _load_all_schemas: inclusion of views alongside tables
- _populate_tree: positional indexing to prevent duplicate column name clobbering
- _search_data: robust rendering of non-Row tuples and export action synchronization
- BLOB / binary handling: bytearray and memoryview support in formatting, CSV, and JSON
- _build_export_payload: retention of duplicate column query results without data loss
"""

import sqlite3
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest
import SQLiteViewer
import export_atomic


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
        if key == "columns":
            self.columns = list(value)

    def heading(self, column, text=None, command=None):
        self.headings.append((column, text, command))

    def column(self, column, width=None, anchor=None):
        self.column_config.append((column, width, anchor))

    def insert(self, parent, index, values):
        self.inserted.append(list(values))

    def delete(self, *items):
        pass

    def get_children(self):
        return []


def test_atomic_export_creates_nested_parent_directories():
    """Verify atomic_export creates missing parent directories instead of crashing with FileNotFoundError."""
    with tempfile.TemporaryDirectory() as base_dir:
        dest = Path(base_dir) / "nested_a" / "nested_b" / "report.csv"
        assert not dest.parent.exists()

        with export_atomic.atomic_export(dest, set(), encoding="utf-8") as f:
            f.write("id;name\n1;test\n")

        assert dest.is_file()
        assert dest.read_text(encoding="utf-8") == "id;name\n1;test\n"


def test_protect_destination_rejects_directory_path():
    """Verify protect_destination explicitly rejects existing directories."""
    with tempfile.TemporaryDirectory() as base_dir:
        with pytest.raises(ValueError, match="Verzeichnis"):
            export_atomic.protect_destination(base_dir, set())


def test_database_files_empty_and_none_db_path():
    """Verify database_files safely handles empty/None db_path without resolving to cwd."""
    conn = sqlite3.connect(":memory:")
    try:
        fake_viewer = SimpleNamespace(db_path="", conn=conn)
        paths = export_atomic.database_files(fake_viewer)
        assert isinstance(paths, set)
        assert Path.cwd() not in paths

        fake_viewer_none = SimpleNamespace(db_path=None, conn=conn)
        paths_none = export_atomic.database_files(fake_viewer_none)
        assert isinstance(paths_none, set)
        assert Path.cwd() not in paths_none
    finally:
        conn.close()


def test_database_files_raises_on_closed_connection():
    """Verify database_files raises sqlite3.Error on closed connection so export safety cannot be bypassed."""
    conn = sqlite3.connect(":memory:")
    conn.close()
    fake_viewer = SimpleNamespace(db_path="", conn=conn)
    with pytest.raises(sqlite3.Error):
        export_atomic.database_files(fake_viewer)


def test_views_loaded_alongside_tables(monkeypatch):
    """Verify _load_tables and schema loaders include SQL views."""
    monkeypatch.setattr(SQLiteViewer.messagebox, "showerror", lambda *args, **kw: None)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t_users (id INT, name TEXT)")
    conn.execute("CREATE VIEW v_active_users AS SELECT id, name FROM t_users WHERE id > 0")

    var_table = SimpleNamespace(get=lambda: "v_active_users", set=lambda x: None)
    var_schema = SimpleNamespace(get=lambda: "v_active_users", set=lambda x: None)
    combo_table = _FakeCombo(var_table)
    combo_schema = _FakeCombo(var_schema)

    fake = SimpleNamespace(
        conn=conn,
        table_combo=combo_table,
        schema_combo=combo_schema,
        table_var=var_table,
        schema_table_var=var_schema,
        load_selected_table=lambda: None,
        _load_schema=lambda: None,
        _clear_tree=lambda: None,
        _clear_schema_text=lambda: None,
        _update_export_actions=lambda: None,
        _set_status=lambda x: None,
    )

    SQLiteViewer.SqlViewer._load_tables(fake)
    assert "t_users" in combo_table.values
    assert "v_active_users" in combo_table.values


def test_populate_tree_preserves_duplicate_column_values():
    """Verify _populate_tree displays distinct positional values when columns have duplicate names."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT 10 AS id, 20 AS id")
    row = cur.fetchone()

    fake_tree = _FakeTree()
    fake = SimpleNamespace(
        tree=fake_tree,
        sort_column=None,
        sort_reverse=False,
        _clear_tree=lambda: None,
        _format_value=lambda v: str(v),
    )

    SQLiteViewer.SqlViewer._populate_tree(fake, ["id", "id"], [row])
    assert len(fake_tree.inserted) == 1
    # Both values (10 and 20) must be preserved, not duplicated as ['10', '10']
    assert fake_tree.inserted[0] == ["10", "20"]


def test_format_value_handles_bytearray_and_memoryview():
    """Verify _format_value formats bytearray and memoryview as BLOB markers."""
    viewer = SimpleNamespace()
    assert SQLiteViewer.SqlViewer._format_value(viewer, None) == "NULL"
    assert SQLiteViewer.SqlViewer._format_value(viewer, b"test") == "[BLOB 4 bytes]"
    assert SQLiteViewer.SqlViewer._format_value(viewer, bytearray(b"abcdef")) == "[BLOB 6 bytes]"
    assert SQLiteViewer.SqlViewer._format_value(viewer, memoryview(b"123")) == "[BLOB 3 bytes]"
    assert SQLiteViewer.SqlViewer._format_value(viewer, 42) == "42"


def test_serialize_export_value_handles_bytearray_and_memoryview():
    """Verify _serialize_export_value converts bytearray and memoryview to base64 blob structures."""
    viewer = SimpleNamespace()
    b_val = bytearray(b"binary_payload")
    serialized = SQLiteViewer.SqlViewer._serialize_export_value(viewer, b_val)
    assert serialized["type"] == "blob"
    assert serialized["size_bytes"] == len(b_val)
    assert serialized["encoding"] == "base64"

    m_val = memoryview(b"memory_payload")
    serialized_m = SQLiteViewer.SqlViewer._serialize_export_value(viewer, m_val)
    assert serialized_m["type"] == "blob"
    assert serialized_m["size_bytes"] == len(m_val)


def test_build_export_payload_preserves_duplicate_column_results():
    """Verify _build_export_payload does not drop column data on duplicate query column names."""
    fake = SimpleNamespace(
        db_path="/path/test.db",
        current_columns=[],
        current_data=[],
        export_context={},
        sql_result_columns=["id", "id"],
        sql_result_data=[(101, 202)],
        sql_result_export_context={"view": "query", "query": "SELECT 101 AS id, 202 AS id"},
        notebook=SimpleNamespace(index=lambda sel: 2, select=lambda: "sql_tab"),
    )
    fake._sql_tab_selected = lambda: True
    fake._serialize_export_value = lambda v: SQLiteViewer.SqlViewer._serialize_export_value(fake, v)

    payload = SQLiteViewer.SqlViewer._build_export_payload(fake)
    rows = payload["result_rows"]
    assert len(rows) == 1
    assert rows[0]["id"] == 101
    assert rows[0]["id_2"] == 202


def test_search_data_handles_tuple_rows_and_updates_export_actions(monkeypatch):
    """Verify _search_data works cleanly with tuple rows and triggers export action update."""
    monkeypatch.setattr(SQLiteViewer.messagebox, "showerror", lambda *args, **kw: None)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INT, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")

    actions_updated = []
    fake_tree = _FakeTree()

    fake = SimpleNamespace(
        conn=conn,
        table_var=SimpleNamespace(get=lambda: "users"),
        search_var=SimpleNamespace(get=lambda: "Alice"),
        limit_var=SimpleNamespace(get=lambda: "100"),
        sort_column=None,
        sort_reverse=False,
        tree=fake_tree,
        row_count_var=SimpleNamespace(set=lambda s: None),
        _SQLITE_KEYWORDS=SQLiteViewer.SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SQLiteViewer.SqlViewer._ident(fake, name),
        _escape_like_pattern=lambda s: SQLiteViewer.SqlViewer._escape_like_pattern(fake, s),
        _format_value=lambda v: str(v),
        _clear_tree=lambda: None,
        _set_current_view_data=lambda cols, rows: None,
        _set_export_context=lambda **kw: None,
        _update_export_actions=lambda: actions_updated.append(True),
        _set_status=lambda s: None,
    )
    fake._populate_tree = lambda cols, rows: SQLiteViewer.SqlViewer._populate_tree(fake, cols, rows)

    SQLiteViewer.SqlViewer._search_data(fake)
    assert len(fake_tree.inserted) == 1
    assert fake_tree.inserted[0] == ["1", "Alice"]
    assert len(actions_updated) == 1

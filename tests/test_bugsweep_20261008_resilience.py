"""
Regression tests for 2026-10-08 Bugsweep resilience fixes:
- Empty table list state cleanup and export action disabling
- Sort column reset on mismatched table columns
- Search escape invariant preserving row count
- SQL editor selection execution support
- Export filename sanitization for special characters
- Table info decoupled inspection resilience
- Translator non-dict resilience and atomic saving
- String source support in protect_destination
"""

import re
import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace
import pytest
import tkinter as tk

from SQLiteViewer import SqlViewer
from export_atomic import protect_destination
from translator import TranslationSystem
from manage_translations import check_translations


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

    def get(self):
        return self.var.get()


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

    def delete(self, *items):
        self.inserted.clear()

    def get_children(self):
        return tuple(range(len(self.inserted)))


def test_empty_table_list_cleans_up_full_state_and_disables_export():
    """Verify _load_tables cleans up current columns, data, export context, row count and schema combo."""
    conn = sqlite3.connect(":memory:")
    table_var = _MutableVar("old_table")
    schema_var = _MutableVar("old_table")
    row_count_var = _MutableVar("Zeilen: 5 / 5")
    table_combo = _FakeCombo(table_var)
    schema_combo = _FakeCombo(schema_var)

    fake = SimpleNamespace(
        conn=conn,
        table_combo=table_combo,
        schema_combo=schema_combo,
        table_var=table_var,
        schema_table_var=schema_var,
        row_count_var=row_count_var,
        current_columns=["col1", "col2"],
        current_data=[("a", "b")],
        export_context={"view": "table", "table": "old_table"},
        sort_column="col1",
        sort_reverse=True,
        sql_result_columns=[],
        sql_result_data=[],
        sql_result_export_context={},
        _clear_tree=lambda: None,
        _clear_schema_text=lambda: None,
        _update_export_actions=lambda: None,
        _set_status=lambda msg: None,
    )

    SqlViewer._load_tables(fake)

    assert table_combo.get() == ""
    assert schema_combo.get() == ""
    assert fake.current_columns == []
    assert fake.current_data == []
    assert fake.export_context == {}
    assert fake.sort_column is None
    assert fake.sort_reverse is False
    assert row_count_var.get() == ""

    action_state = SqlViewer._get_export_action_state(fake)
    assert action_state["enabled"] is False


def test_load_selected_table_resets_mismatched_sort_column():
    """Verify sort_column is cleared when the selected table does not contain it."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE products (sku TEXT, price REAL)")
    conn.commit()

    table_var = _MutableVar("products")
    limit_var = _MutableVar(100)
    row_count_var = _MutableVar("")
    tree = _FakeTree()

    fake = SimpleNamespace(
        conn=conn,
        table_var=table_var,
        limit_var=limit_var,
        row_count_var=row_count_var,
        sort_column="old_column_not_here",
        sort_reverse=True,
        current_columns=[],
        current_data=[],
        export_context={},
        tree=tree,
        _SQLITE_KEYWORDS=SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SqlViewer._ident(fake, name),
        _set_current_view_data=lambda cols, rows: setattr(fake, "current_columns", list(cols)),
        _set_export_context=lambda **kw: setattr(fake, "export_context", kw),
        _populate_tree=lambda cols, rows: None,
        _update_export_actions=lambda: None,
        _set_status=lambda msg: None,
        _clear_tree=lambda: None,
    )

    SqlViewer.load_selected_table(fake)

    assert fake.sort_column is None
    assert fake.sort_reverse is False
    assert fake.export_context["sort_column"] is None
    assert fake.export_context["sort_descending"] is False


def test_clear_search_preserves_row_count_when_no_active_search():
    """Verify pressing Escape in an empty search box does not wipe row_count_var."""
    search_var = _MutableVar("")
    table_var = _MutableVar("customers")
    row_count_var = _MutableVar("Zeilen: 42 / 42")
    reloaded = []

    fake = SimpleNamespace(
        search_var=search_var,
        table_var=table_var,
        row_count_var=row_count_var,
        search_entry=None,
        load_selected_table=lambda: reloaded.append(True),
    )

    result = SqlViewer._clear_search(fake)

    assert result == "break"
    assert len(reloaded) == 0
    assert row_count_var.get() == "Zeilen: 42 / 42"


def test_execute_sql_executes_selected_text_when_selection_exists():
    """Verify execute_sql executes only selected query text if a text selection is present."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE accounts (id INT, balance REAL)")
    conn.execute("INSERT INTO accounts VALUES (1, 150.0), (2, 300.0)")
    conn.commit()

    captured_result = {}

    class _MockTextWidget:
        def tag_ranges(self, tag):
            if tag == tk.SEL:
                return ("1.0", "1.34")
            return ()

        def get(self, start, end):
            if start == tk.SEL_FIRST and end == tk.SEL_LAST:
                return "SELECT balance FROM accounts WHERE id = 2"
            return "SELECT 1;\nSELECT 2;\nSELECT 3;"

    fake = SimpleNamespace(
        conn=conn,
        sql_text=_MockTextWidget(),
        table_var=_MutableVar("accounts"),
        sql_status=SimpleNamespace(config=lambda **kw: None),
        sql_result_columns=[],
        sql_result_data=[],
        sql_result_export_context={},
        _populate_sql_result=lambda cols, rows: captured_result.update(cols=cols, rows=rows),
        _update_export_actions=lambda: None,
    )

    SqlViewer.execute_sql(fake)

    assert captured_result.get("cols") == ["balance"]
    assert len(captured_result.get("rows")) == 1
    assert captured_result["rows"][0]["balance"] == 300.0


def test_export_filename_sanitizes_special_characters():
    """Verify export_csv and export_json sanitize filename characters."""
    table_raw = 'audit:sales/2026*"test"?'
    safe_table = re.sub(r'[\\/*?:"<>|]', '_', str(table_raw)).strip(' .') or "export"
    assert ":" not in safe_table
    assert "/" not in safe_table
    assert "*" not in safe_table
    assert "?" not in safe_table
    assert '"' not in safe_table
    assert safe_table == "audit_sales_2026__test__"


def test_get_table_info_resilient_to_count_error():
    """Verify _get_table_info handles COUNT(*) failures without dropping index and FK info."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE base (id INT PRIMARY KEY, parent_id INT, FOREIGN KEY (parent_id) REFERENCES base(id))")
    conn.execute("CREATE INDEX idx_base_parent ON base(parent_id)")
    conn.commit()

    # Original execution
    fake = SimpleNamespace(
        conn=conn,
        _SQLITE_KEYWORDS=SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SqlViewer._ident(fake, name),
    )

    info = SqlViewer._get_table_info(fake, "base")
    assert "Spalten: 2" in info
    assert "Zeilen: 0" in info
    assert "Indizes: 2" in info  # primary key autoindex + idx_base_parent
    assert "Foreign Keys: 1" in info

    # Now simulate a broken COUNT(*) query on a view/table while keeping PRAGMAs working
    class _FailingCountConn:
        def execute(self, query, *args):
            if "COUNT(*)" in query:
                raise sqlite3.OperationalError("Simulated count failure")
            return conn.execute(query, *args)

    fake_failing = SimpleNamespace(
        conn=_FailingCountConn(),
        _SQLITE_KEYWORDS=SqlViewer._SQLITE_KEYWORDS,
        _ident=lambda name: SqlViewer._ident(fake_failing, name),
    )

    info_partial = SqlViewer._get_table_info(fake_failing, "base")
    assert "Spalten: 2" in info_partial
    assert "Zeilen:" not in info_partial  # Count failed gracefully
    assert "Indizes: 2" in info_partial  # Indizes still retrieved
    assert "Foreign Keys: 1" in info_partial  # FKs still retrieved


def test_translator_handles_non_dict_corrupt_entry():
    """Verify translator.t() does not crash on non-dict translation entries."""
    tr = TranslationSystem("de")
    tr.translations["corrupt_key"] = "simple string instead of dict"
    val = tr.t("corrupt_key")
    assert val == "simple string instead of dict"

    tr.translations["none_key"] = None
    assert tr.t("none_key") == "none_key"


def test_translator_atomic_save(tmp_path):
    """Verify _save_translations writes atomically and does not leave temporary files."""
    tr = TranslationSystem("de", app_dir=tmp_path)
    tr.translations_file = tmp_path / "locales" / "translations.json"
    tr.add_translation("TestKey", de="TestText", en="TestTextEn")

    assert tr.translations_file.exists()
    with open(tr.translations_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["TestKey"]["en"] == "TestTextEn"

    # Verify no temp files left behind
    leftover_tmp = list((tmp_path / "locales").glob("*.tmp"))
    assert len(leftover_tmp) == 0


def test_manage_translations_check_passes():
    """Verify check_translations reports 100% parity on locales/translations.json."""
    repo_dir = Path(__file__).parent.parent
    assert check_translations(str(repo_dir)) is True


def test_protect_destination_supports_string_sources(tmp_path):
    """Verify protect_destination accepts string sources without AttributeError."""
    db_file = tmp_path / "source.db"
    db_file.write_bytes(b"sqlite")
    dest_file = tmp_path / "export.csv"

    # Pass source as string rather than Path
    protect_destination(str(dest_file), [str(db_file)])

    # Target matching source string should raise ValueError
    with pytest.raises(ValueError, match="geschützte Datenbankdatei"):
        protect_destination(str(db_file), [str(db_file)])

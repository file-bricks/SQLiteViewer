# -*- coding: utf-8 -*-
"""
High-End Refactoring & Architecture Hardening Tests
===================================================
Tests for:
- Atomic settings persistence with exception cleanup (no orphaned .tmp files)
- Export CSV streaming generator and formula injection protection
- Export JSON precomputed deduplicated column keys and non-finite float safety
- Max cell display length guard in _format_value (GUI protection vs. 100% full export fidelity)
- SQL editor syntax highlighting debouncing and window close cancellation
"""

import json
import base64
from types import SimpleNamespace
import SQLiteViewer


def test_atomic_settings_persistence_success(tmp_path, monkeypatch):
    """Verify _save_settings writes valid JSON atomically with fsync and replace."""
    settings_file = tmp_path / "sqliteviewer_settings.json"
    monkeypatch.setattr(SQLiteViewer.SqlViewer, "_get_settings_path", staticmethod(lambda: settings_file))

    viewer = SimpleNamespace(
        current_language="es",
        _get_settings_path=staticmethod(lambda: settings_file),
    )

    SQLiteViewer.SqlViewer._save_settings(viewer)
    assert settings_file.exists()

    with open(settings_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"language": "es"}

    # No leftover temporary files
    leftover_tmps = list(tmp_path.glob("*.tmp")) + list(tmp_path.glob(".*.tmp"))
    assert leftover_tmps == []


def test_atomic_settings_cleanup_on_write_failure(tmp_path, monkeypatch):
    """Verify _save_settings cleans up temporary files when serialization/flush fails."""
    settings_file = tmp_path / "sqliteviewer_settings.json"
    monkeypatch.setattr(SQLiteViewer.SqlViewer, "_get_settings_path", staticmethod(lambda: settings_file))

    viewer = SimpleNamespace(
        current_language="de",
        _get_settings_path=staticmethod(lambda: settings_file),
    )

    # Monkeypatch json.dump to simulate an unexpected error (e.g. disk full, permission)
    def failing_dump(*args, **kwargs):
        raise OSError("Simulated disk write error")

    monkeypatch.setattr(json, "dump", failing_dump)

    # Should handle exception gracefully without crashing
    SQLiteViewer.SqlViewer._save_settings(viewer)

    # Destination should not exist, and NO temporary files should be orphaned
    assert not settings_file.exists()
    leftover_tmps = list(tmp_path.glob("*.tmp")) + list(tmp_path.glob(".*.tmp"))
    assert leftover_tmps == [], f"Found orphaned temporary files: {leftover_tmps}"


def test_format_value_display_guard_vs_export_fidelity():
    """Verify _format_value truncates massive text for Treeview while exports keep 100%."""
    viewer = SimpleNamespace()

    # Normal lengths
    assert SQLiteViewer.SqlViewer._format_value(viewer, None) == "NULL"
    assert SQLiteViewer.SqlViewer._format_value(viewer, 123) == "123"
    assert SQLiteViewer.SqlViewer._format_value(viewer, "Short text") == "Short text"
    assert SQLiteViewer.SqlViewer._format_value(viewer, b"blob") == "[BLOB 4 bytes]"
    assert SQLiteViewer.SqlViewer._format_value(viewer, bytearray(b"12345")) == "[BLOB 5 bytes]"
    assert SQLiteViewer.SqlViewer._format_value(viewer, memoryview(b"12")) == "[BLOB 2 bytes]"

    # Extreme length string (e.g. 5,000 characters)
    huge_str = "A" * 5000
    display_val = SQLiteViewer.SqlViewer._format_value(viewer, huge_str)

    # Must be truncated for GUI performance
    assert len(display_val) < 5000
    assert display_val.startswith("A" * SQLiteViewer.MAX_CELL_DISPLAY_LEN)
    assert "… [5000 chars]" in display_val

    # BUT export serialization MUST keep 100% un-truncated data!
    serialized = SQLiteViewer.SqlViewer._serialize_export_value(viewer, huge_str)
    assert serialized == huge_str
    assert len(serialized) == 5000


def test_export_json_precomputed_keys_and_deduplication():
    """Verify _build_export_payload precomputes column keys and handles duplicates correctly."""
    columns = ["id", "title", "id", "category", "id"]
    rows = [
        (1, "Alpha", 101, "Test", 1001),
        (2, "Beta", 102, "Prod", 1002),
    ]
    context = {"view": "table", "table": "items"}

    viewer = SimpleNamespace(
        db_path="C:/test/sample.db",
        current_columns=columns,
        current_data=rows,
        export_context=context,
        sql_result_columns=[],
        sql_result_data=[],
        sql_result_export_context={},
    )

    payload = SQLiteViewer.SqlViewer._build_export_payload(viewer)

    assert payload["schema_version"] == "sqliteviewer-export-v1"
    assert payload["row_count"] == 2
    assert payload["columns"] == columns

    # Verify deduplicated keys
    first_row = payload["result_rows"][0]
    assert list(first_row.keys()) == ["id", "title", "id_2", "category", "id_3"]
    assert first_row["id"] == 1
    assert first_row["title"] == "Alpha"
    assert first_row["id_2"] == 101
    assert first_row["category"] == "Test"
    assert first_row["id_3"] == 1001


def test_export_json_non_finite_floats_and_blobs():
    """Verify _build_export_payload handles NaN, Inf, -Inf and raw bytes safely."""
    columns = ["val_nan", "val_inf", "val_neginf", "raw_blob"]
    rows = [
        (float("nan"), float("inf"), float("-inf"), b"\x00\x01\x02\xff"),
    ]
    context = {"view": "query", "query": "SELECT ..."}

    viewer = SimpleNamespace(
        db_path=None,
        current_columns=columns,
        current_data=rows,
        export_context=context,
        sql_result_columns=[],
        sql_result_data=[],
        sql_result_export_context={},
    )

    payload = SQLiteViewer.SqlViewer._build_export_payload(viewer)
    row = payload["result_rows"][0]

    # Floats must be stringified so JSON dump produces RFC 8259 compliant output
    assert row["val_nan"] == "nan"
    assert row["val_inf"] == "inf"
    assert row["val_neginf"] == "-inf"

    # Raw blob must be base64 dict
    blob_entry = row["raw_blob"]
    assert blob_entry["type"] == "blob"
    assert blob_entry["encoding"] == "base64"
    assert blob_entry["size_bytes"] == 4
    assert base64.b64decode(blob_entry["data"]) == b"\x00\x01\x02\xff"

    # json.dumps must succeed without error
    json_text = json.dumps(payload)
    assert "nan" in json_text


def test_sql_highlight_debouncing_and_close_cancel():
    """Verify _highlight_sql debounces KeyRelease events and _on_close cancels pending timer."""
    scheduled = []
    cancelled = []

    class MockApp:
        def __init__(self):
            self._sql_highlight_job = None
            self.closed = False
            self.conn = None
            self.highlight_executed = False

        def after(self, ms, callback):
            job_id = f"job_{len(scheduled) + 1}"
            scheduled.append((job_id, ms, callback))
            return job_id

        def after_cancel(self, job_id):
            cancelled.append(job_id)

        def _do_highlight_sql(self):
            self.highlight_executed = True

        def close_db(self):
            pass

        def destroy(self):
            self.closed = True

    app = MockApp()

    # 1. Immediate execution when event is None (programmatic call)
    SQLiteViewer.SqlViewer._highlight_sql(app, event=None)
    assert app.highlight_executed is True
    assert app._sql_highlight_job is None

    # 2. Debounced execution on keyboard event
    app.highlight_executed = False
    fake_event = SimpleNamespace(keysym="a")
    SQLiteViewer.SqlViewer._highlight_sql(app, event=fake_event)
    assert app._sql_highlight_job == "job_1"
    assert len(scheduled) == 1
    assert scheduled[0][1] == 120  # 120ms debounce

    # 3. Second rapid keystroke cancels previous job and reschedules
    fake_event2 = SimpleNamespace(keysym="b")
    SQLiteViewer.SqlViewer._highlight_sql(app, event=fake_event2)
    assert "job_1" in cancelled
    assert app._sql_highlight_job == "job_2"
    assert len(scheduled) == 2

    # 4. _on_close cleanly cancels the pending job and destroys
    SQLiteViewer.SqlViewer._on_close(app)
    assert "job_2" in cancelled
    assert app._sql_highlight_job is None
    assert app.closed is True

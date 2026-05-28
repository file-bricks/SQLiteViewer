from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "_WARTUNG" / "generate_store_screenshots.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("sqliteviewer_store_screenshots", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_create_demo_database_builds_expected_tables(tmp_path):
    module = _load_module()
    db_path = tmp_path / "demo.sqlite"

    module.create_demo_database(db_path)

    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        project_count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        note_count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

    assert tables == {"projects", "notes"}
    assert project_count == 3
    assert note_count == 3


def test_write_manifest_lists_all_expected_screenshots(tmp_path):
    module = _load_module()

    module.write_manifest(tmp_path)

    content = (tmp_path / "README.md").read_text(encoding="utf-8")
    for filename, caption in module.SCREENSHOTS:
        assert filename in content
        assert caption in content

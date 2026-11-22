"""Regression tests for fail-closed behavior in manage_translations.py."""

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

import manage_translations as mt


def test_manage_translations_aborts_on_corrupt_json_without_overwriting(tmp_path: Path) -> None:
    locales_dir = tmp_path / "locales"
    locales_dir.mkdir(parents=True)
    trans_file = locales_dir / "translations.json"
    raw = "{corrupt-json"
    trans_file.write_text(raw, encoding="utf-8")
    (tmp_path / "app.py").write_text('label = QLabel("Fehler beim Öffnen")\n', encoding="utf-8")

    ok = mt.manage_translations(str(tmp_path))

    assert ok is False
    assert trans_file.read_text(encoding="utf-8") == raw


def test_manage_translations_aborts_on_non_dict_json_without_overwriting(tmp_path: Path) -> None:
    locales_dir = tmp_path / "locales"
    locales_dir.mkdir(parents=True)
    trans_file = locales_dir / "translations.json"
    raw = '["unexpected", "list"]'
    trans_file.write_text(raw, encoding="utf-8")

    ok = mt.manage_translations(str(tmp_path))

    assert ok is False
    assert trans_file.read_text(encoding="utf-8") == raw
    assert mt.check_translations(str(tmp_path)) is False


def test_manage_translations_cli_exits_nonzero_on_corrupt_json(tmp_path: Path) -> None:
    locales_dir = tmp_path / "locales"
    locales_dir.mkdir(parents=True)
    trans_file = locales_dir / "translations.json"
    trans_file.write_text("{broken", encoding="utf-8")
    script = Path(mt.__file__).resolve()

    proc = subprocess.run(
        [sys.executable, str(script), "--dir", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 1
    assert trans_file.read_text(encoding="utf-8") == "{broken"


def test_manage_translations_preserves_existing_and_adds_new_atomically(tmp_path: Path) -> None:
    locales_dir = tmp_path / "locales"
    locales_dir.mkdir(parents=True)
    trans_file = locales_dir / "translations.json"
    trans_file.write_text(
        json.dumps({"Speichern": {"de": "Speichern", "en": "Save"}}, ensure_ascii=False),
        encoding="utf-8",
    )
    (tmp_path / "ui.py").write_text('btn = QPushButton("Datei öffnen")\n', encoding="utf-8")

    ok = mt.manage_translations(str(tmp_path))

    assert ok is True
    data = json.loads(trans_file.read_text(encoding="utf-8"))
    assert data["Speichern"]["en"] == "Save"
    assert data["Datei öffnen"]["de"] == "Datei öffnen"
    assert not list(locales_dir.glob(".translations.*.tmp"))


def test_manage_translations_aborts_on_non_utf8_file_without_overwriting(tmp_path: Path) -> None:
    locales_dir = tmp_path / "locales"
    locales_dir.mkdir(parents=True)
    trans_file = locales_dir / "translations.json"
    raw = '{"Übersetzung": {"de": "Übersetzung"}}'.encode("utf-16")
    trans_file.write_bytes(raw)

    ok = mt.manage_translations(str(tmp_path))

    assert ok is False
    assert trans_file.read_bytes() == raw


@pytest.mark.skipif(os.name == "nt", reason="POSIX-Dateirechte")
def test_atomic_write_preserves_existing_file_mode(tmp_path: Path) -> None:
    trans_file = tmp_path / "translations.json"
    trans_file.write_text("{}", encoding="utf-8")
    os.chmod(trans_file, 0o644)

    mt._atomic_write_json(str(trans_file), {"a": {"de": "a"}})

    assert stat.S_IMODE(os.stat(trans_file).st_mode) == 0o644
    assert json.loads(trans_file.read_text(encoding="utf-8")) == {"a": {"de": "a"}}

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests für GUI Language Switching Contract, Dynamic Retranslate & Settings Persistence
(SV-I18N-01 .. SV-I18N-04, SV-I18N-06)
"""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import SQLiteViewer
from translator import TranslationSystem


def test_translation_system_supported_languages_list():
    """Prüft, ob TranslationSystem alle 6 geforderten Sprachen unterstützt."""
    expected = {"de", "en", "es", "zh", "ja", "ru"}
    assert set(TranslationSystem.SUPPORTED_LANGUAGES) == expected


def test_sqlviewer_settings_load_and_save(tmp_path, monkeypatch):
    """Prüft, ob _load_settings und _save_settings die sqliteviewer_settings.json korrekt lesen/schreiben."""
    settings_file = tmp_path / "sqliteviewer_settings.json"
    monkeypatch.setattr(SQLiteViewer.SqlViewer, "_get_settings_path", staticmethod(lambda: settings_file))

    viewer = SimpleNamespace(
        current_language="es",
        _get_settings_path=staticmethod(lambda: settings_file),
    )

    # 1. Speichern
    SQLiteViewer.SqlViewer._save_settings(viewer)
    assert settings_file.exists()

    with open(settings_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"language": "es"}

    # 2. Laden
    loaded = SQLiteViewer.SqlViewer._load_settings(viewer)
    assert loaded == {"language": "es"}


def test_sqlviewer_detect_system_language(monkeypatch):
    """Prüft die Fallback-Erkennung der Systemsprache."""
    monkeypatch.setattr("locale.getlocale", lambda: ("es_ES", "UTF-8"))
    assert SQLiteViewer.SqlViewer._detect_system_language() == "es"

    monkeypatch.setattr("locale.getlocale", lambda: ("zh_CN", "UTF-8"))
    assert SQLiteViewer.SqlViewer._detect_system_language() == "zh"

    monkeypatch.setattr("locale.getlocale", lambda: ("ja_JP", "UTF-8"))
    assert SQLiteViewer.SqlViewer._detect_system_language() == "ja"

    monkeypatch.setattr("locale.getlocale", lambda: ("ru_RU", "UTF-8"))
    assert SQLiteViewer.SqlViewer._detect_system_language() == "ru"

    monkeypatch.setattr("locale.getlocale", lambda: ("en_US", "UTF-8"))
    assert SQLiteViewer.SqlViewer._detect_system_language() == "en"

    monkeypatch.setattr("locale.getlocale", lambda: ("de_DE", "UTF-8"))
    assert SQLiteViewer.SqlViewer._detect_system_language() == "de"


def test_sqlviewer_tr_fallback():
    """Prüft die tr() Methode mit TranslationSystem und bei fehlendem Translator."""
    # Mit Translator
    translator = TranslationSystem(default_lang="en")
    viewer = SimpleNamespace(translator=translator)

    assert SQLiteViewer.SqlViewer.tr(viewer, "Tabelle:") == "Table:"
    assert SQLiteViewer.SqlViewer.tr(viewer, "Limit:") == "Limit:"
    assert SQLiteViewer.SqlViewer.tr(viewer, "UnbekannterKey123") == "UnbekannterKey123"

    # Ohne Translator (z. B. im Mock/Fake Kontext)
    fake_viewer = SimpleNamespace()
    assert SQLiteViewer.SqlViewer.tr(fake_viewer, "Tabelle:") == "Tabelle:"


def test_sqlviewer_change_language_and_retranslate_ui(tmp_path, monkeypatch):
    """Prüft den dynamischen Sprachwechsel ohne Neustart und die Aktualisierung aller UI-Komponenten."""
    settings_file = tmp_path / "sqliteviewer_settings.json"
    monkeypatch.setattr(SQLiteViewer.SqlViewer, "_get_settings_path", staticmethod(lambda: settings_file))

    # Mock Widgets
    table_label = MagicMock()
    limit_label = MagicMock()
    search_label = MagicMock()
    refresh_button = MagicMock()
    export_button = MagicMock()
    notebook = MagicMock()
    schema_table_label = MagicMock()
    schema_all_btn = MagicMock()
    sql_input_frame = MagicMock()
    sql_run_btn = MagicMock()
    sql_clear_btn = MagicMock()
    sql_result_frame = MagicMock()
    status_var = MagicMock()
    status_var.get.return_value = "Bereit"
    lang_var = MagicMock()

    menubar = MagicMock()
    file_menu = MagicMock()
    edit_menu = MagicMock()
    view_menu = MagicMock()
    help_menu = MagicMock()

    translator = TranslationSystem(default_lang="de")

    viewer = SimpleNamespace(
        translator=translator,
        current_language="de",
        title=MagicMock(),
        _get_settings_path=staticmethod(lambda: settings_file),
        _save_settings=lambda: SQLiteViewer.SqlViewer._save_settings(viewer),
        _load_settings=lambda: SQLiteViewer.SqlViewer._load_settings(viewer),
        tr=lambda k: SQLiteViewer.SqlViewer.tr(viewer, k),
        change_language=lambda lang: SQLiteViewer.SqlViewer.change_language(viewer, lang),
        retranslate_ui=lambda: SQLiteViewer.SqlViewer.retranslate_ui(viewer),
        _set_status=MagicMock(),
        _update_export_actions=MagicMock(),
        table_label=table_label,
        limit_label=limit_label,
        search_label=search_label,
        refresh_button=refresh_button,
        export_button=export_button,
        notebook=notebook,
        schema_table_label=schema_table_label,
        schema_all_btn=schema_all_btn,
        sql_input_frame=sql_input_frame,
        sql_run_btn=sql_run_btn,
        sql_clear_btn=sql_clear_btn,
        sql_result_frame=sql_result_frame,
        status_var=status_var,
        lang_var=lang_var,
        menubar=menubar,
        file_menu=file_menu,
        edit_menu=edit_menu,
        view_menu=view_menu,
        help_menu=help_menu,
    )

    # 1. Wechsel auf Englisch
    viewer.change_language("en")

    assert viewer.current_language == "en"
    assert translator.get_language() == "en"
    lang_var.set.assert_called_with("en")

    # Prüfe UI Aktualisierungen
    table_label.configure.assert_called_with(text="Table:")
    limit_label.configure.assert_called_with(text="Limit:")
    search_label.configure.assert_called_with(text="Search:")
    refresh_button.configure.assert_called_with(text="⟳ Refresh")

    # Tabs
    notebook.tab.assert_any_call(0, text="📊 Data")
    notebook.tab.assert_any_call(1, text="🔧 Schema")
    notebook.tab.assert_any_call(2, text="💻 SQL Editor")

    # Menüs
    menubar.entryconfigure.assert_any_call(1, label="File")
    menubar.entryconfigure.assert_any_call(2, label="Edit")
    menubar.entryconfigure.assert_any_call(3, label="View")
    menubar.entryconfigure.assert_any_call(4, label="Help")

    file_menu.entryconfigure.assert_any_call(0, label="Open Database…")
    file_menu.entryconfigure.assert_any_call(1, label="Close Database")
    file_menu.entryconfigure.assert_any_call(6, label="Exit")

    edit_menu.entryconfigure.assert_any_call(0, label="Find…")
    edit_menu.entryconfigure.assert_any_call(1, label="Select All")
    edit_menu.entryconfigure.assert_any_call(3, label="Refresh")

    view_menu.entryconfigure.assert_any_call(0, label="Data Tab")
    view_menu.entryconfigure.assert_any_call(1, label="Schema Tab")
    view_menu.entryconfigure.assert_any_call(2, label="SQL-Editor")
    view_menu.entryconfigure.assert_any_call(4, label="Language")

    help_menu.entryconfigure.assert_any_call(0, label="About…")

    # Status
    status_var.set.assert_called_with("Ready")

    # Settings persistiert
    with open(settings_file, "r", encoding="utf-8") as f:
        saved = json.load(f)
    assert saved == {"language": "en"}

    # 2. Wechsel auf Spanisch
    status_var.get.return_value = "Ready"
    viewer.change_language("es")
    assert viewer.current_language == "es"
    table_label.configure.assert_called_with(text="Tabla:")
    refresh_button.configure.assert_called_with(text="⟳ Actualizar")
    status_var.set.assert_called_with("Listo")

    # 3. Wechsel auf Russisch
    status_var.get.return_value = "Listo"
    viewer.change_language("ru")
    assert viewer.current_language == "ru"
    table_label.configure.assert_called_with(text="Таблица:")
    refresh_button.configure.assert_called_with(text="⟳ Обновить")
    status_var.set.assert_called_with("Готово")

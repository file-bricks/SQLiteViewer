#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests für UX-, Accessibility- & Tastatur-Ergonomie (WCAG 2.1 AA / BITV 2.0)
für SQLiteViewer Pro (SV-UX-01 .. SV-UX-08).
"""

from types import SimpleNamespace
from unittest.mock import MagicMock
from pathlib import Path
import tkinter as tk

import SQLiteViewer
from SQLiteViewer import ToolTip, SqlViewer
import manage_translations


def test_tooltip_creation_and_text_update():
    """Prüft, ob ToolTip korrekt instanziiert wird, Events bindet und set_text unterstützt."""
    mock_widget = MagicMock(spec=tk.Widget)
    app = SimpleNamespace(_set_status=MagicMock())

    tip = ToolTip(mock_widget, text="Suchfeld", app=app, status_text="Volltextsuche")

    assert tip.text == "Suchfeld"
    assert tip.status_text == "Volltextsuche"
    assert tip.app is app

    # Prüfe Bindings
    bound_events = [call[0][0] for call in mock_widget.bind.call_args_list]
    for expected in ["<Enter>", "<Leave>", "<FocusIn>", "<FocusOut>", "<ButtonPress>", "<Escape>"]:
        assert expected in bound_events

    # FocusIn Statusbar-Echo
    tip._on_focus_in()
    app._set_status.assert_called_with("Volltextsuche")

    # set_text
    tip.set_text("Neuer Text", "Neuer Statustext")
    assert tip.text == "Neuer Text"
    assert tip.status_text == "Neuer Statustext"

    # hide_tip
    tip.hide_tip()
    assert tip.tip_window is None


def test_menubar_mnemonics_and_accelerators(monkeypatch):
    """Prüft, ob Menüleiste und Untermenüs Alt-Mnemonics (underline) und Tastenkürzel aufweisen."""
    viewer = SimpleNamespace(
        tr=lambda k: k,
        config=MagicMock(),
        bind_all=MagicMock(),
        open_db=MagicMock(),
        close_db=MagicMock(),
        _on_close=MagicMock(),
        export_csv=MagicMock(),
        export_json=MagicMock(),
        _focus_search=MagicMock(),
        _select_all=MagicMock(),
        load_selected_table=MagicMock(),
        _switch_tab=MagicMock(),
        show_shortcuts_help=MagicMock(),
        show_about_dialog=MagicMock(),
    )

    def _fake_menu(parent=None, **kwargs):
        m = MagicMock()
        m.index.return_value = 0
        return m

    monkeypatch.setattr(SQLiteViewer.tk, "Menu", _fake_menu)
    monkeypatch.setattr(SQLiteViewer.tk, "StringVar", lambda **kwargs: MagicMock())

    SqlViewer._build_menu(viewer)

    # Prüfe, dass Menüpunkte Shortcuts gebunden haben
    bound_keys = [call[0][0] for call in viewer.bind_all.call_args_list]
    for key in [
        "<Control-o>", "<Control-w>", "<Control-q>", "<Control-e>",
        "<Control-f>", "<Control-a>", "<F5>", "<F1>", "<Shift-F1>",
        "<Control-1>", "<Control-2>", "<Control-3>", "<Control-Shift-E>",
    ]:
        assert key in bound_keys, f"Fehlendes Tastenkürzel: {key}"


def test_shortcuts_help_dialog_content_and_parity(monkeypatch):
    """Prüft, ob show_shortcuts_help alle Kategorien, Shortcuts und Barrierefreiheitshinweise enthält."""
    shown_boxes = []

    def fake_showinfo(title, message):
        shown_boxes.append((title, message))

    monkeypatch.setattr(SQLiteViewer.messagebox, "showinfo", fake_showinfo)

    viewer = SimpleNamespace(
        tr=lambda k: k,
    )

    SqlViewer.show_shortcuts_help(viewer)

    assert len(shown_boxes) == 1
    title, message = shown_boxes[0]

    assert "Tastaturkürzel" in title
    assert "Globale Tastaturkürzel" in message
    assert "Strg + O" in message
    assert "Strg + W" in message
    assert "Strg + E" in message
    assert "Strg + F" in message
    assert "F5" in message
    assert "F9" in message
    assert "F1" in message
    assert "Shift + F1" in message
    assert "WCAG 2.1 AA" in message
    assert "Tooltips" in message


def test_about_dialog_content_and_invariants(monkeypatch):
    """Prüft, ob show_about_dialog Version 2.1.0, Lizenz, Local-First und Zero-Egress Invarianten benennt."""
    shown_boxes = []

    def fake_showinfo(title, message):
        shown_boxes.append((title, message))

    monkeypatch.setattr(SQLiteViewer.messagebox, "showinfo", fake_showinfo)

    viewer = SimpleNamespace(
        tr=lambda k: k,
    )

    SqlViewer.show_about_dialog(viewer)

    assert len(shown_boxes) == 1
    title, message = shown_boxes[0]

    assert "SQLite Viewer" in title
    assert "2.1.0" in message
    assert "Zero-Egress" in message
    assert "MIT" in message
    assert "WCAG 2.1 AA" in message


def test_switch_tab_navigation():
    """Prüft den barrierefreien Tab-Wechsel."""
    mock_notebook = MagicMock()
    viewer = SimpleNamespace(notebook=mock_notebook)

    SqlViewer._switch_tab(viewer, 0)
    mock_notebook.select.assert_called_with(0)

    SqlViewer._switch_tab(viewer, 2)
    mock_notebook.select.assert_called_with(2)


def test_dynamic_retranslation_updates_tooltips_and_menus():
    """Prüft, ob retranslate_ui alle registrierten Tooltips und Menüelemente aktualisiert."""
    tip1 = MagicMock()
    tip2 = MagicMock()

    help_menu = MagicMock()
    status_var = MagicMock()
    status_var.get.return_value = "Bereit"

    viewer = SimpleNamespace(
        title=MagicMock(),
        tr=lambda k: f"[{k}]",
        _tooltips=[(tip1, "Tabelle auswählen", "Tabelle auswählen"), (tip2, "SQL-Eingabe leeren", "SQL-Eingabe leeren")],
        help_menu=help_menu,
        status_var=status_var,
        _update_export_actions=MagicMock(),
    )

    SqlViewer.retranslate_ui(viewer)

    tip1.set_text.assert_called_with("[Tabelle auswählen]", "[Tabelle auswählen]")
    tip2.set_text.assert_called_with("[SQL-Eingabe leeren]", "[SQL-Eingabe leeren]")
    help_menu.entryconfigure.assert_any_call(0, label="[Über…]")
    help_menu.entryconfigure.assert_any_call(1, label="[Tastaturkürzel & Barrierefreiheit…]")


def test_translations_check_ci_gate():
    """Prüft, ob der Übersetzungskatalog alle 6 geforderten Sprachen ohne Lücken abdeckt."""
    repo_root = Path(__file__).parent.parent
    result = manage_translations.check_translations(str(repo_root))
    assert result is True, "manage_translations.check_translations() muss 100% Parität für DE, EN, ES, ZH, JA, RU bestätigen"

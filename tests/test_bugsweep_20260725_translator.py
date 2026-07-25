# -*- coding: utf-8 -*-
"""Regressionstest — Bugsweep 2026-07-25: TranslationSystem Fallback bei leeren Übersetzungs-Strings."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from translator import TranslationSystem


def test_t_returns_fallback_when_translation_value_is_empty_string(tmp_path):
    """
    Beweis des Bugs: Wenn in translations.json ein Eintrag {"de": "Tabelle", "en": ""} existiert,
    gibt tr.t("Tabelle") im EN-Modus "" (leeren String) zurück anstelle des deutschen Fallbacks.
    """
    ts = TranslationSystem(default_lang="en", app_dir=tmp_path)
    ts.translations["Tabelle"] = {"de": "Tabelle", "en": ""}

    result = ts.t("Tabelle")
    assert result == "Tabelle", f"Erwartet Fallback 'Tabelle', bekam {result!r}"

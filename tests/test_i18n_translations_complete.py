"""
Unit-Test für Vollständigkeit der 6-Sprachen-Übersetzungen (DE, EN, ES, ZH, JA, RU).
"""

import json
from pathlib import Path
from translator import TranslationSystem


def test_translations_json_completeness():
    translations_file = Path(__file__).parent.parent / "locales" / "translations.json"
    assert translations_file.exists(), "locales/translations.json muss existieren"

    with open(translations_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) > 0, "translations.json darf nicht leer sein"

    required_langs = TranslationSystem.SUPPORTED_LANGUAGES

    for key, lang_dict in data.items():
        for lang in required_langs:
            assert lang in lang_dict, f"Key '{key}' fehlt Sprache '{lang}'"
            assert lang_dict[lang] != "", f"Key '{key}' hat leere Übersetzung für '{lang}'"


def test_translation_system_loads_all_languages(tmp_path):
    tr = TranslationSystem(default_lang='es', app_dir=Path(__file__).parent.parent)

    assert tr.t("Datenbank öffnen…") == "Abrir base de datos…"

    tr.set_language('zh')
    assert tr.t("Datenbank öffnen…") == "打开数据库…"

    tr.set_language('ja')
    assert tr.t("Datenbank öffnen…") == "データベースを開く…"

    tr.set_language('ru')
    assert tr.t("Datenbank öffnen…") == "Открыть базу данных…"

    tr.set_language('en')
    assert tr.t("Datenbank öffnen…") == "Open Database…"

    tr.set_language('de')
    assert tr.t("Datenbank öffnen…") == "Datenbank öffnen…"

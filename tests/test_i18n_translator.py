"""
Unit-Tests für TranslationSystem in DATA/REL-PUB_SQLiteViewer
==============================================================
Testet Multi-Language-Unterstützung (DE, EN, ES, ZH, JA, RU),
Fallback-Verhalten und Härtung von set_language() / add_translation().
"""

import json
from pathlib import Path
from translator import TranslationSystem


def test_translation_system_supported_languages(tmp_path):
    tr = TranslationSystem(default_lang='es', app_dir=tmp_path)
    assert tr.get_language() == 'es'
    assert 'es' in tr.get_supported_languages()
    assert 'zh' in tr.get_supported_languages()
    assert 'ja' in tr.get_supported_languages()
    assert 'ru' in tr.get_supported_languages()


def test_translation_fallback_chain(tmp_path):
    tr = TranslationSystem(default_lang='es', app_dir=tmp_path)
    tr.add_translation(
        key="Datenbank öffnen",
        de="Datenbank öffnen",
        en="Open Database",
        es="Abrir base de datos",
        zh="打开数据库",
        ja="データベースを開く",
        ru="Открыть базу данных"
    )

    assert tr.t("Datenbank öffnen") == "Abrir base de datos"

    tr.set_language('zh')
    assert tr.t("Datenbank öffnen") == "打开数据库"

    tr.set_language('ja')
    assert tr.t("Datenbank öffnen") == "データベースを開く"

    tr.set_language('ru')
    assert tr.t("Datenbank öffnen") == "Открыть базу данных"

    tr.set_language('en')
    assert tr.t("Datenbank öffnen") == "Open Database"

    tr.set_language('de')
    assert tr.t("Datenbank öffnen") == "Datenbank öffnen"


def test_translation_fallback_when_language_missing(tmp_path):
    tr = TranslationSystem(default_lang='es', app_dir=tmp_path)
    # Entry with EN and DE, but empty ES
    tr.translations["Exportieren"] = {
        "de": "Exportieren",
        "en": "Export",
        "es": "",
        "zh": "",
        "ja": "",
        "ru": ""
    }

    # Should fallback to EN ("Export") when current_lang is ES
    assert tr.t("Exportieren") == "Export"

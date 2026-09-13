"""
TranslationSystem - Multi-Language Support fuer Anwendungen
============================================================
Version: 1.1.0 (gehaertet & I18N-erweitert)
Quelle: DATA/REL-PUB_SQLiteViewer/translator.py

Verwendung:
-----------
from translator import TranslationSystem

translator = TranslationSystem('de')
label.setText(translator.t('Datei oeffnen'))
translator.set_language('en')
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set


class TranslationSystem:
    """Multi-Language Support System v1.1.0"""

    SUPPORTED_LANGUAGES = ['de', 'en', 'es', 'zh', 'ja', 'ru']

    def __init__(self, default_lang: str = 'de', app_dir: Path = None):
        """
        Initialisiert Translation-System.

        Args:
            default_lang: Standard-Sprache ('de', 'en', 'es', 'zh', 'ja', 'ru')
            app_dir: Verzeichnis der Anwendung (default: aktuelles Verzeichnis)
        """
        self.current_lang = default_lang if default_lang in self.SUPPORTED_LANGUAGES else 'de'

        if app_dir is None:
            app_dir = Path.cwd()
        self.app_dir = Path(app_dir)

        self.translations_file = self.app_dir / "locales" / "translations.json"

        self.string_patterns = [
            re.compile(r'setText\s*\(\s*["\']([^"\']+)["\']\s*\)'),
            re.compile(r'setWindowTitle\s*\(\s*["\']([^"\']+)["\']\s*\)'),
            re.compile(r'QLabel\s*\(\s*["\']([^"\']+)["\']\s*\)'),
            re.compile(r'QPushButton\s*\(\s*["\']([^"\']+)["\']\s*\)'),
            re.compile(r'addAction\s*\([^,]*["\']([^"\']+)["\']\s*\)'),
            re.compile(r'addTab\s*\([^,]+,\s*["\']([^"\']+)["\']\s*\)'),
            re.compile(r'text\s*=\s*"([^"]+)"'),
        ]

        self.german_hints = [
            "datei", "bearbeiten", "ansicht", "hilfe", "oeffnen", "speichern",
            "schliessen", "einstellungen", "abbrechen", "ok", "ja", "nein",
            "start", "stop", "pause", "fortsetzen", "laden", "aktualisieren",
            "filter", "fehler", "export", "import", "optionen", "anzeigen",
        ]

        self.translations = {}
        self._load_translations()

    def _load_translations(self):
        if self.translations_file.exists():
            try:
                with open(self.translations_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
            except Exception:
                self.translations = {}
        else:
            self.translations = {}

    def _save_translations(self):
        # Bugsweep: bei nicht-beschreibbarem Dateisystem (z.B. installiert unter Program Files)
        # nicht abstuerzen — _save_translations wird aus UI-Callbacks (t()/add_translation) gerufen.
        try:
            self.translations_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.translations_file, 'w', encoding='utf-8') as f:
                json.dump(self.translations, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

    def t(self, key: str) -> str:
        """
        Uebersetzt einen Key in die aktuelle Sprache. Fallback auf EN, DE oder den Key.

        Args:
            key: Translation-Key (oft der deutsche Originaltext)

        Returns:
            Uebersetzter Text oder Key als Fallback
        """
        if key in self.translations:
            lang_dict = self.translations[key]
            val = lang_dict.get(self.current_lang)
            if val:
                return val
            val_en = lang_dict.get('en')
            if val_en:
                return val_en
            return lang_dict.get('de') or key

        if self._is_german(key):
            self.translations[key] = {lang: (key if lang == 'de' else "") for lang in self.SUPPORTED_LANGUAGES}
            self._save_translations()

        return key

    def set_language(self, lang: str):
        if lang in self.SUPPORTED_LANGUAGES:
            self.current_lang = lang

    def get_language(self) -> str:
        return self.current_lang

    def get_supported_languages(self) -> List[str]:
        return list(self.SUPPORTED_LANGUAGES)

    def add_translation(self, key: str, de: str = "", en: str = "", es: str = "", zh: str = "", ja: str = "", ru: str = ""):
        self.translations[key] = {
            "de": de or key,
            "en": en or "",
            "es": es or "",
            "zh": zh or "",
            "ja": ja or "",
            "ru": ru or "",
        }
        self._save_translations()

    def scan_and_update(self, project_dir: Path = None) -> Dict:
        """Scannt Projekt-Dateien nach deutschen Strings und aktualisiert translations.json."""
        if project_dir is None:
            project_dir = self.app_dir
        else:
            project_dir = Path(project_dir)

        found_strings = self._find_german_strings(project_dir)

        added = []
        for string in sorted(found_strings):
            if string not in self.translations:
                self.translations[string] = {lang: (string if lang == 'de' else "") for lang in self.SUPPORTED_LANGUAGES}
                added.append(string)

        if added:
            self._save_translations()

        missing = [k for k, v in self.translations.items() if not v.get("en")]

        return {'added': added, 'missing': missing, 'total': len(self.translations)}

    def _find_german_strings(self, directory: Path) -> Set[str]:
        directory = Path(directory)
        german_strings = set()
        skip_dirs = {'build', 'dist', 'venv', '.venv', '__pycache__', 'releases'}

        for py_file in directory.rglob("*.py"):
            if any(folder in py_file.parts for folder in skip_dirs):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue

            for pattern in self.string_patterns:
                for match in pattern.findall(content):
                    if match and self._is_german(match):
                        german_strings.add(match.strip())

        return german_strings

    def _is_german(self, text: str) -> bool:
        if any(ch in text for ch in "äöüÄÖÜß"):
            return True
        text_lower = text.lower()
        return any(hint in text_lower for hint in self.german_hints)

    def get_missing_translations(self) -> List[str]:
        return [k for k, v in self.translations.items() if not v.get("en")]


if __name__ == "__main__":
    tr = TranslationSystem('de')
    print(f"Sprache: {tr.get_language()}")
    result = tr.scan_and_update()
    print(f"Scan: {result['total']} Strings, {len(result['added'])} neu, {len(result['missing'])} ohne EN")


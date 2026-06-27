"""Regressionstests — bugfix-library-transfer 2026-06-21."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import manage_translations as mt


class TestU2ManageTranslations(unittest.TestCase):
    """BUG-U2: json.load ohne JSONDecodeError-Handler in manage_translations."""

    def test_corrupted_json_does_not_raise(self):
        """Korrupte translations.json darf keine unkontrollierte Exception werfen."""
        with tempfile.TemporaryDirectory() as tmpdir:
            locales_dir = os.path.join(tmpdir, "locales")
            os.makedirs(locales_dir)
            with open(os.path.join(locales_dir, "translations.json"), "w", encoding="utf-8") as f:
                f.write("{corrupted json")
            try:
                mt.manage_translations(tmpdir)
            except json.JSONDecodeError:
                self.fail("JSONDecodeError nicht gefangen — BUG-U2 in manage_translations")


if __name__ == "__main__":
    unittest.main()

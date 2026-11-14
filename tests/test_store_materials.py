# -*- coding: utf-8 -*-
"""Hermetische Vertragstests für Windows Store Packaging, Tier-2 6-Sprachen-Staging & Policy 10.1.3."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "scripts" / "check_store_readiness.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("sqliteviewer_check_store_readiness", CHECKER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _copy_store_fixture(tmp_path: Path) -> Path:
    """Kopiert alle Store-relevanten Text- und Asset-Dateien hermetisch nach tmp_path."""
    rel_files = [
        "store_package.json",
        "STORE_LISTING.md",
        "WINDOWS_STORE_PREP.md",
        "PRIVACY_POLICY.md",
        "SQLiteViewer.ico",
        "store_package/SQLite Viewer Pro/AppxManifest.xml",
        "store_package/SQLite Viewer Pro/icons/icon_44x44.png",
        "store_package/SQLite Viewer Pro/icons/icon_50x50.png",
        "store_package/SQLite Viewer Pro/icons/icon_150x150.png",
        "store_package/SQLite Viewer Pro/icons/icon_310x150.png",
        "store_package/SQLite Viewer Pro/icons/icon_310x310.png",
        "releases/windowsstore/store_settings.json",
        "releases/windowsstore/BUILD.md",
        "releases/windowsstore/WACK_PROTOCOL.md",
        "releases/windowsstore/StoreLogo.png",
        "releases/windowsstore/store_listing_de.md",
        "releases/windowsstore/store_listing_en.md",
        "releases/windowsstore/store_listing_es.md",
        "releases/windowsstore/store_listing_zh.md",
        "releases/windowsstore/store_listing_ja.md",
        "releases/windowsstore/store_listing_ru.md",
    ]
    for rel in rel_files:
        src = REPO_ROOT / rel
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    store_assets_dst = tmp_path / "store_assets"
    shutil.copytree(REPO_ROOT / "store_assets", store_assets_dst)
    return tmp_path


def test_store_readiness_preflight_passes_zero_findings():
    checker = _load_checker()
    passed, findings = checker.check_store_readiness(REPO_ROOT)
    assert findings == [], f"Unerwartete Store-Readiness-Mängel: {findings}"
    assert len(passed) >= 45


def test_store_readiness_cli_json_output():
    proc = subprocess.run(
        [sys.executable, str(CHECKER_PATH), "--json"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["finding_count"] == 0
    assert payload["passed_count"] >= 45


def test_store_package_and_settings_exact_tier2_parity():
    pkg = json.loads((REPO_ROOT / "store_package.json").read_text(encoding="utf-8"))
    settings = json.loads(
        (REPO_ROOT / "releases" / "windowsstore" / "store_settings.json").read_text(encoding="utf-8")
    )

    assert pkg["version"] == "2.1.0.0"
    assert settings["version"] == "2.1.0.0"
    assert pkg["identity_name"] == "Geiger.SQLiteViewerPro"
    assert settings["identity_name"] == "Geiger.SQLiteViewerPro"
    assert pkg["store_id"] == "9P6H501XB8JT"
    assert settings["store_id"] == "9P6H501XB8JT"

    for code in ("de", "en", "es", "zh", "ja", "ru"):
        desc = pkg[f"description_{code}"]
        assert 10 <= len(desc) <= 100
        assert settings[f"description_{code}"] == desc

        kws = pkg[f"keywords_{code}"]
        assert len(kws) == 7
        assert len({k.lower() for k in kws}) == 7, f"Duplikate in keywords_{code}: {kws}"
        assert all(1 <= len(k) <= 30 for k in kws)
        assert settings[f"keywords_{code}"] == kws


def test_checker_rejects_policy_10_1_3_trademark_and_length_violations(tmp_path):
    checker = _load_checker()
    fixture = _copy_store_fixture(tmp_path)

    pkg_path = fixture / "store_package.json"
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    pkg["description_de"] = "X" * 101
    pkg["descriptions"]["de-DE"] = pkg["description_de"]
    pkg["keywords_en"][0] = "dbeaver alternative"
    pkg["keywords"]["en-US"] = list(pkg["keywords_en"])
    pkg["keywords_es"].append("extra achter begriff")
    pkg_path.write_text(json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8")

    build_md = fixture / "releases" / "windowsstore" / "BUILD.md"
    synthetic_user_dir = "\\".join(("C:", "Users", "Alice", "Desktop"))
    build_md.write_text(build_md.read_text(encoding="utf-8") + f"\ncd {synthetic_user_dir}\n", encoding="utf-8")

    _passed, findings = checker.check_store_readiness(fixture)
    joined = "\n".join(findings)
    assert "description_de überschreitet 100 Zeichen" in joined
    assert "Richtlinie 10.1.3" in joined
    assert "keywords_es muss exakt 7 Begriffe enthalten" in joined
    assert "Enthält lokale Benutzerpfade" in joined


def test_staged_windowsstore_files_not_git_ignored():
    staged_paths = [
        "WINDOWS_STORE_PREP.md",
        "scripts/check_store_readiness.py",
        "store_assets/StoreLogo.png",
        "store_assets/Square50x50Logo.png",
        "releases/windowsstore/BUILD.md",
        "releases/windowsstore/WACK_PROTOCOL.md",
        "releases/windowsstore/store_settings.json",
        "releases/windowsstore/StoreLogo.png",
        "releases/windowsstore/store_listing_de.md",
        "releases/windowsstore/store_listing_en.md",
        "releases/windowsstore/store_listing_es.md",
        "releases/windowsstore/store_listing_zh.md",
        "releases/windowsstore/store_listing_ja.md",
        "releases/windowsstore/store_listing_ru.md",
    ]
    proc = subprocess.run(
        ["git", "check-ignore", *staged_paths],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=15,
        check=False,
    )
    # git check-ignore exits with code 1 when NO supplied path is ignored
    assert proc.returncode == 1, f"Staging-Dateien fälschlich von .gitignore ausgeschlossen:\n{proc.stdout}"

    # Gleichzeitig müssen Binärpakete und interne Portierungspläne strikt ignoriert bleiben
    ignored_probe = subprocess.run(
        [
            "git",
            "check-ignore",
            "PORTIERUNGSPLAN.md",
            "AUFGABEN.txt",
            "releases/SQLiteViewer.msix",
            "releases/windowsstore/v2.1.0/SQLiteViewerPro-2.1.0.0.msix",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=15,
        check=False,
    )
    assert ignored_probe.returncode == 0
    ignored_lines = {line.strip() for line in ignored_probe.stdout.splitlines() if line.strip()}
    assert "PORTIERUNGSPLAN.md" in ignored_lines
    assert "AUFGABEN.txt" in ignored_lines

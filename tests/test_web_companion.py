# -*- coding: utf-8 -*-
"""Hermetische Vertragstests für den SQLiteViewer Web/PWA-Companion (Target 3)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = REPO_ROOT / "web_companion"
EXPECTED_LOCALES = ("de", "en", "es", "zh", "ja", "ru")


def test_web_companion_core_files_and_bilingual_readme_parity():
    required = (
        "index.html",
        "app.js",
        "library.js",
        "i18n.js",
        "style.css",
        "sw.js",
        "manifest.webmanifest",
        "package.json",
        "README.md",
        "README_de.md",
    )
    for rel in required:
        path = WEB_DIR / rel
        assert path.is_file(), f"Pflichtdatei fehlt in web_companion/: {rel}"
        assert path.stat().st_size > 50, f"Datei unerwartet leer: {rel}"

    readme_en = (WEB_DIR / "README.md").read_text(encoding="utf-8")
    readme_de = (WEB_DIR / "README_de.md").read_text(encoding="utf-8")
    assert "README_de.md" in readme_en, "web_companion/README.md muss auf README_de.md verweisen"
    assert "README.md" in readme_de, "web_companion/README_de.md muss auf README.md verweisen"
    assert "source.database_path" in readme_en, "web_companion/README.md muss source.database_path dokumentieren"
    assert "source.database_path" in readme_de, "web_companion/README_de.md muss source.database_path dokumentieren"


def test_web_companion_zero_egress_and_no_external_cdns():
    """Stellt sicher, dass HTML, CSS und JS keinerlei externe URLs oder Netzwerk-Uploads laden."""
    for rel in ("index.html", "app.js", "library.js", "i18n.js", "style.css"):
        text = (WEB_DIR / rel).read_text(encoding="utf-8")
        ext_urls = re.findall(r"https?://[^\s\"')>]+", text, flags=re.IGNORECASE)
        assert ext_urls == [], f"Externe URL in {rel} verletzt Offline-First/Zero-Egress: {ext_urls}"

    for js_rel in ("app.js", "library.js", "i18n.js"):
        js_text = (WEB_DIR / js_rel).read_text(encoding="utf-8")
        for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket(", "navigator.sendBeacon"):
            assert forbidden not in js_text, f"Verbotener Netzwerkaufruf {forbidden} in {js_rel}"


def test_web_companion_manifest_and_service_worker_assets_exist():
    manifest = json.loads((WEB_DIR / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert manifest.get("display") == "standalone"
    for icon in manifest.get("icons", []):
        icon_src = icon["src"].lstrip("./")
        assert (WEB_DIR / icon_src).is_file(), f"Manifest-Icon fehlt physisch: {icon_src}"

    sw_text = (WEB_DIR / "sw.js").read_text(encoding="utf-8")
    array_match = re.search(r"OFFLINE_ASSETS\s*=\s*\[([\s\S]*?)\]", sw_text)
    assert array_match is not None, "OFFLINE_ASSETS nicht in sw.js gefunden"
    assets = re.findall(r'"([^"]+)"', array_match.group(1))
    assert "./i18n.js" in assets, "sw.js muss ./i18n.js für den Offline-Start cachen"
    assert "./app.js" in assets
    assert "./library.js" in assets

    for asset in assets:
        if asset == "./":
            continue
        rel = asset[2:] if asset.startswith("./") else asset
        assert (WEB_DIR / rel).is_file(), f"Service-Worker-Asset fehlt auf der Festplatte: {asset}"


def test_web_companion_tier2_6_languages_dom_and_dictionary():
    html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
    lang_buttons = re.findall(r'data-lang-btn="([a-z]{2})"', html)
    assert tuple(lang_buttons) == EXPECTED_LOCALES

    i18n_js = (WEB_DIR / "i18n.js").read_text(encoding="utf-8")
    for loc in EXPECTED_LOCALES:
        assert re.search(rf"^\s*{loc}\s*:\s*\{{", i18n_js, flags=re.MULTILINE), (
            f"Sprachblock '{loc}' fehlt in web_companion/i18n.js"
        )


def test_web_companion_node_test_suite_passes():
    node_bin = shutil.which("node")
    if not node_bin:
        pytest.skip("Node.js ist in dieser Umgebung nicht installiert")

    proc = subprocess.run(
        [node_bin, "--test", "tests/library.test.mjs", "tests/pwa.test.mjs", "tests/i18n.test.mjs"],
        cwd=str(WEB_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=45,
        check=False,
    )
    assert proc.returncode == 0, f"Node-Companion-Tests fehlgeschlagen:\n{proc.stdout}\n{proc.stderr}"

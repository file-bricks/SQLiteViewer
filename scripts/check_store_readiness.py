#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Store-Readiness Preflight Checker für SQLite Viewer Pro.

Prüft ohne externe Laufzeitabhängigkeiten (100 % Python-Standardbibliothek) alle
Windows-Store-Artefakte auf Vollständigkeit, Manifest-/Versionskonsistenz,
Icon-/Kachel-Maßhaltigkeit (PNG IHDR & ICO Header), Pfad-Hygiene sowie
Policy-P-006 Tier-2 6-Sprachen-Parität und Microsoft Partner Center Richtlinie 10.1.3.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_APP_NAME = "SQLite Viewer Pro"
EXPECTED_IDENTITY = "Geiger.SQLiteViewerPro"
EXPECTED_PUBLISHER = "CN=52596601-BAB4-4F3F-B182-E8F3F273B202"
EXPECTED_STORE_ID = "9P6H501XB8JT"
EXPECTED_VERSION = "2.1.0.0"
EXPECTED_EXECUTABLE = "SQLiteViewer.exe"
EXPECTED_ALIAS = "sqliteviewer.exe"
EXPECTED_EXTENSIONS = {".db", ".sqlite", ".sqlite3"}

TIER2_LANGUAGES = ("de-DE", "en-US", "es-ES", "zh-CN", "ja-JP", "ru-RU")
TIER2_LANG_CODES = ("de", "en", "es", "zh", "ja", "ru")
LANG_CODE_TO_TAG = dict(zip(TIER2_LANG_CODES, TIER2_LANGUAGES))

# Fremde Marken- und Wettbewerbsbegriffe, die gemäß Microsoft Partner Center
# Richtlinie 10.1.3 weder in Store-Keywords noch als vergleichende Nennung im
# Store-Listing auftauchen dürfen.
FORBIDDEN_TRADEMARKS = {
    "microsoft",
    "windows",
    "apple",
    "macos",
    "google",
    "android",
    "ios",
    "dbeaver",
    "db browser",
    "db browser for sqlite",
    "sqlitestudio",
    "navicat",
    "datagrip",
    "heidisql",
    "excel",
    "access",
    "java",
}

USER_PATH_RE = re.compile(
    r"([a-zA-Z]:\\Users\\[a-zA-Z0-9_\-\\]+|/home/[a-zA-Z0-9_\-]+)",
    re.IGNORECASE,
)


def read_png_dimensions(path: Path) -> tuple[int, int]:
    """Liest Breite und Höhe direkt aus dem PNG-IHDR-Header (ohne Pillow)."""
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"Ungültiger PNG-Header in {path}")
    width, height = struct.unpack(">II", data[16:24])
    return int(width), int(height)


def read_ico_sizes(path: Path) -> set[tuple[int, int]]:
    """Liest alle eingebetteten Frame-Größen aus dem ICO-Directory-Header."""
    data = path.read_bytes()
    if len(data) < 6:
        raise ValueError(f"Zu kurze ICO-Datei: {path}")
    reserved, ico_type, count = struct.unpack("<HHH", data[:6])
    if reserved != 0 or ico_type != 1 or count < 1:
        raise ValueError(f"Ungültiger ICO-Header in {path}")
    if len(data) < 6 + count * 16:
        raise ValueError(f"Abgeschnittener ICO-Directory-Block in {path}")
    sizes: set[tuple[int, int]] = set()
    for idx in range(count):
        offset = 6 + idx * 16
        w_raw, h_raw = data[offset], data[offset + 1]
        width = 256 if w_raw == 0 else int(w_raw)
        height = 256 if h_raw == 0 else int(h_raw)
        sizes.add((width, height))
    return sizes


def _extract_numbered_keywords(block: str) -> list[str]:
    keywords: list[str] = []
    for raw_line in block.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r"^\d+\.\s*(.+)$", line)
        if match:
            keywords.append(match.group(1).strip())
    return keywords


def _contains_forbidden_trademark(text: str) -> str | None:
    lowered = text.lower()
    for brand in sorted(FORBIDDEN_TRADEMARKS, key=len, reverse=True):
        if re.search(rf"(?<!\w){re.escape(brand)}(?!\w)", lowered):
            return brand
    return None


def check_store_readiness(project_root: Path = PROJECT_ROOT) -> tuple[list[str], list[str]]:
    """Führt alle Windows-Store-Preflight-Prüfungen für SQLite Viewer Pro aus.

    Returns:
        tuple[list[str], list[str]]: (passed_checks, findings)
    """
    passed: list[str] = []
    findings: list[str] = []

    pkg_data: dict | None = None

    # 1. store_package.json
    pkg_file = project_root / "store_package.json"
    if not pkg_file.is_file():
        findings.append("store_package.json fehlt im Projektroot.")
    else:
        try:
            pkg_data = json.loads(pkg_file.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(f"store_package.json ist kein valides JSON: {exc}")

    if isinstance(pkg_data, dict):
        req_fields = (
            "app_name",
            "identity_name",
            "publisher",
            "publisher_display",
            "version",
            "description",
            "executable",
            "execution_alias",
            "capabilities",
            "category",
            "age_rating",
            "license",
            "languages",
            "privacy_url",
            "support_url",
            "store_id",
        )
        missing = [f for f in req_fields if not pkg_data.get(f)]
        if missing:
            findings.append(f"store_package.json: Fehlende Pflichtfelder: {missing}")
        else:
            passed.append("store_package.json: Pflichtfelder vollständig")

        checks_exact = (
            ("app_name", EXPECTED_APP_NAME),
            ("identity_name", EXPECTED_IDENTITY),
            ("publisher", EXPECTED_PUBLISHER),
            ("store_id", EXPECTED_STORE_ID),
            ("version", EXPECTED_VERSION),
            ("executable", EXPECTED_EXECUTABLE),
            ("execution_alias", EXPECTED_ALIAS),
        )
        for key, expected in checks_exact:
            actual = pkg_data.get(key)
            if actual != expected:
                findings.append(f"store_package.json: '{key}' ist '{actual}', erwartet '{expected}'")
            else:
                passed.append(f"store_package.json: {key} == '{expected}'")

        for url_key in ("privacy_url", "support_url"):
            url_val = str(pkg_data.get(url_key, ""))
            if not url_val.startswith("https://"):
                findings.append(f"store_package.json: '{url_key}' muss mit https:// beginnen")
            else:
                passed.append(f"store_package.json: {url_key} ist gültige HTTPS-URL")

        exts = set((pkg_data.get("file_types") or {}).get("extensions") or [])
        if exts != EXPECTED_EXTENSIONS:
            findings.append(f"store_package.json: file_types.extensions ist {sorted(exts)}, erwartet {sorted(EXPECTED_EXTENSIONS)}")
        else:
            passed.append("store_package.json: Dateizuordnungen (.db, .sqlite, .sqlite3) vollständig")

        langs = pkg_data.get("languages") or []
        if list(langs) != list(TIER2_LANGUAGES):
            findings.append(f"store_package.json: languages ist {langs}, erwartet {list(TIER2_LANGUAGES)}")
        else:
            passed.append("store_package.json: Alle 6 Tier-2-Sprachen in kanonischer Reihenfolge deklariert")

        descriptions_map = pkg_data.get("descriptions") or {}
        keywords_map = pkg_data.get("keywords") or {}

        for code in TIER2_LANG_CODES:
            tag = LANG_CODE_TO_TAG[code]
            desc_val = pkg_data.get(f"description_{code}")
            desc_map_val = descriptions_map.get(tag)
            if not isinstance(desc_val, str) or not desc_val.strip():
                findings.append(f"store_package.json: description_{code} fehlt oder ist leer")
            elif len(desc_val) > 100:
                findings.append(f"store_package.json: description_{code} überschreitet 100 Zeichen ({len(desc_val)})")
            elif desc_map_val != desc_val:
                findings.append(f"store_package.json: descriptions['{tag}'] weicht von description_{code} ab")
            else:
                passed.append(f"store_package.json: description_{code} ({len(desc_val)}/100 Zeichen) synchron")

            kw_val = pkg_data.get(f"keywords_{code}")
            kw_map_val = keywords_map.get(tag)
            if not isinstance(kw_val, list) or len(kw_val) != 7:
                findings.append(
                    f"store_package.json: keywords_{code} muss exakt 7 Begriffe enthalten "
                    f"(gefunden: {len(kw_val) if isinstance(kw_val, list) else 'kein Array'})"
                )
            elif kw_map_val != kw_val:
                findings.append(f"store_package.json: keywords['{tag}'] weicht von keywords_{code} ab")
            else:
                kw_errors = False
                for kw in kw_val:
                    if not isinstance(kw, str) or not kw.strip():
                        findings.append(f"store_package.json: Leeres Keyword in keywords_{code}")
                        kw_errors = True
                    elif len(kw) > 30:
                        findings.append(f"store_package.json: Keyword '{kw}' in keywords_{code} > 30 Zeichen ({len(kw)})")
                        kw_errors = True
                    else:
                        hit = _contains_forbidden_trademark(kw)
                        if hit:
                            findings.append(
                                f"store_package.json: Keyword '{kw}' in keywords_{code} verletzt Richtlinie 10.1.3 (Marke '{hit}')"
                            )
                            kw_errors = True
                if not kw_errors:
                    passed.append(f"store_package.json: keywords_{code} (7/7 Begriffe, <=30 Zeichen, Policy 10.1.3 OK)")

    # 2. releases/windowsstore/store_settings.json Synchronität
    settings_file = project_root / "releases" / "windowsstore" / "store_settings.json"
    if not settings_file.is_file():
        findings.append("releases/windowsstore/store_settings.json fehlt.")
    else:
        try:
            settings_data = json.loads(settings_file.read_text(encoding="utf-8"))
            if isinstance(pkg_data, dict):
                sync_keys = (
                    "app_name",
                    "package_id",
                    "identity_name",
                    "publisher",
                    "publisher_display",
                    "store_id",
                    "version",
                    "executable",
                    "execution_alias",
                    "capabilities",
                    "category",
                    "age_rating",
                    "license",
                    "privacy_url",
                    "support_url",
                    "languages",
                    "file_types",
                    "descriptions",
                    "keywords",
                ) + tuple(f"description_{c}" for c in TIER2_LANG_CODES) + tuple(
                    f"keywords_{c}" for c in TIER2_LANG_CODES
                )
                drifted = [k for k in sync_keys if settings_data.get(k) != pkg_data.get(k)]
                if drifted:
                    findings.append(f"store_settings.json weicht von store_package.json ab in Feldern: {drifted}")
                else:
                    passed.append("releases/windowsstore/store_settings.json ist zu 100 % synchron mit store_package.json")
        except Exception as exc:
            findings.append(f"releases/windowsstore/store_settings.json Lesefehler: {exc}")

    # 3. AppxManifest.xml
    manifest_file = project_root / "store_package" / "SQLite Viewer Pro" / "AppxManifest.xml"
    if not manifest_file.is_file():
        findings.append("store_package/SQLite Viewer Pro/AppxManifest.xml fehlt.")
    else:
        try:
            tree = ET.parse(manifest_file)
            root = tree.getroot()
            ns = {
                "m": "http://schemas.microsoft.com/appx/manifest/foundation/windows10",
                "uap": "http://schemas.microsoft.com/appx/manifest/uap/windows10",
                "desktop": "http://schemas.microsoft.com/appx/manifest/desktop/windows10",
                "rescap": "http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities",
            }
            identity = root.find("m:Identity", ns)
            if identity is None:
                findings.append("AppxManifest.xml: <Identity> fehlt.")
            else:
                id_checks = (
                    ("Name", EXPECTED_IDENTITY),
                    ("Publisher", EXPECTED_PUBLISHER),
                    ("Version", EXPECTED_VERSION),
                    ("ProcessorArchitecture", "x64"),
                )
                for attr, exp in id_checks:
                    got = identity.attrib.get(attr)
                    if got != exp:
                        findings.append(f"AppxManifest.xml: Identity {attr}='{got}', erwartet '{exp}'")
                    else:
                        passed.append(f"AppxManifest.xml: Identity {attr} == '{exp}'")

            res_langs = [
                el.attrib.get("Language", "")
                for el in root.findall("m:Resources/m:Resource", ns)
            ]
            missing_res = [lang for lang in TIER2_LANGUAGES if lang not in res_langs]
            if missing_res:
                findings.append(f"AppxManifest.xml: Fehlende Resource-Sprachen: {missing_res}")
            else:
                passed.append("AppxManifest.xml: Alle 6 Tier-2 Resource-Sprachen vorhanden")

            full_trust = root.find("m:Capabilities/rescap:Capability[@Name='runFullTrust']", ns)
            if full_trust is None:
                findings.append("AppxManifest.xml: rescap:Capability runFullTrust fehlt.")
            else:
                passed.append("AppxManifest.xml: runFullTrust Capability deklariert")

            ft_elems = root.findall(".//uap:SupportedFileTypes/uap:FileType", ns)
            ft_vals = {el.text.strip() for el in ft_elems if el.text}
            if ft_vals != EXPECTED_EXTENSIONS:
                findings.append(f"AppxManifest.xml: SupportedFileTypes {sorted(ft_vals)} != {sorted(EXPECTED_EXTENSIONS)}")
            else:
                passed.append("AppxManifest.xml: FileTypeAssociation (.db, .sqlite, .sqlite3) vollständig")

            alias_el = root.find(".//desktop:ExecutionAlias", ns)
            if alias_el is None or alias_el.attrib.get("Alias") != EXPECTED_ALIAS:
                findings.append("AppxManifest.xml: ExecutionAlias 'sqliteviewer.exe' fehlt.")
            else:
                passed.append("AppxManifest.xml: AppExecutionAlias 'sqliteviewer.exe' vorhanden")

            default_tile = root.find(".//uap:DefaultTile", ns)
            if default_tile is None:
                findings.append("AppxManifest.xml: <uap:DefaultTile> fehlt.")
            else:
                if not default_tile.attrib.get("Wide310x150Logo") or not default_tile.attrib.get("Square310x310Logo"):
                    findings.append("AppxManifest.xml: DefaultTile muss Wide310x150Logo und Square310x310Logo referenzieren.")
                else:
                    passed.append("AppxManifest.xml: DefaultTile referenziert Wide310x150Logo & Square310x310Logo")
        except Exception as exc:
            findings.append(f"AppxManifest.xml XML-Parse-Fehler: {exc}")

    # 4. PNG- & ICO-Assets (Maßhaltigkeit ohne externe Abhängigkeiten)
    ico_path = project_root / "SQLiteViewer.ico"
    if not ico_path.is_file():
        findings.append("SQLiteViewer.ico fehlt im Projektroot.")
    else:
        try:
            ico_sizes = read_ico_sizes(ico_path)
            if (256, 256) not in ico_sizes or not ({(16, 16), (32, 32), (48, 48)} & ico_sizes):
                findings.append(f"SQLiteViewer.ico: Erwartete Multi-Frame-Größen unvollständig ({sorted(ico_sizes)})")
            else:
                passed.append(f"SQLiteViewer.ico: Multi-Frame-ICO valide ({len(ico_sizes)} Auflösungen inkl. 256x256)")
        except Exception as exc:
            findings.append(f"SQLiteViewer.ico Fehler: {exc}")

    required_pngs = (
        ("store_assets/Square44x44Logo.png", (44, 44)),
        ("store_assets/Square50x50Logo.png", (50, 50)),
        ("store_assets/StoreLogo.png", (50, 50)),
        ("store_assets/Square150x150Logo.png", (150, 150)),
        ("store_assets/Wide310x150Logo.png", (310, 150)),
        ("store_assets/Square310x310Logo.png", (310, 310)),
        ("store_package/SQLite Viewer Pro/icons/icon_44x44.png", (44, 44)),
        ("store_package/SQLite Viewer Pro/icons/icon_50x50.png", (50, 50)),
        ("store_package/SQLite Viewer Pro/icons/icon_150x150.png", (150, 150)),
        ("store_package/SQLite Viewer Pro/icons/icon_310x150.png", (310, 150)),
        ("store_package/SQLite Viewer Pro/icons/icon_310x310.png", (310, 310)),
        ("releases/windowsstore/StoreLogo.png", (50, 50)),
    )
    png_errors = 0
    for rel_path, expected_dim in required_pngs:
        fpath = project_root / rel_path
        if not fpath.is_file():
            findings.append(f"Store-Asset fehlt: {rel_path}")
            png_errors += 1
        else:
            try:
                dim = read_png_dimensions(fpath)
                if dim != expected_dim:
                    findings.append(f"Store-Asset {rel_path} hat Maße {dim}, erwartet {expected_dim}")
                    png_errors += 1
            except Exception as exc:
                findings.append(f"Store-Asset {rel_path} ungültig: {exc}")
                png_errors += 1
    if png_errors == 0:
        passed.append(f"Alle {len(required_pngs)} Store-Kachel- und Logo-PNGs vorhanden und exakt maßhaltig")

    targetsize_pngs = list((project_root / "store_assets").glob("Square44x44Logo.targetsize-*.png"))
    if len(targetsize_pngs) < 30:
        findings.append(f"store_assets/: Zu wenige targetsize-Icons gefunden ({len(targetsize_pngs)}, erwartet >= 30)")
    else:
        passed.append(f"store_assets/: {len(targetsize_pngs)} Square44x44Logo.targetsize-Varianten vorhanden")

    # 5. STORE_LISTING.md Richtlinie 10.1.3 & 6-Sprachen-Prüfung
    listing_path = project_root / "STORE_LISTING.md"
    if not listing_path.is_file():
        findings.append("STORE_LISTING.md fehlt.")
    else:
        listing_text = listing_path.read_text(encoding="utf-8")
        hit_body = _contains_forbidden_trademark(listing_text)
        if hit_body:
            findings.append(
                f"STORE_LISTING.md enthält geschützten Fremdmarken-/Wettbewerbsbegriff '{hit_body}' (Richtlinie 10.1.3)."
            )
        else:
            passed.append("STORE_LISTING.md ist frei von fremden Marken- und Wettbewerbsbegriffen (Richtlinie 10.1.3)")

        section_specs = (
            ("de", r"## Deutsch[\s\S]*?### Kurzbeschreibung[^\n]*\n([^\n]+)[\s\S]*?### Suchbegriffe[^\n]*\n([\s\S]*?)(?=### Kategorie)"),
            ("en", r"## English[\s\S]*?### Short Description[^\n]*\n([^\n]+)[\s\S]*?### Search Keywords[^\n]*\n([\s\S]*?)(?=### Category)"),
            ("es", r"## Español[\s\S]*?### Descripción corta[^\n]*\n([^\n]+)[\s\S]*?### Palabras clave[^\n]*\n([\s\S]*?)(?=### Categoría)"),
            ("zh", r"## 简体中文[\s\S]*?### 简短描述[^\n]*\n([^\n]+)[\s\S]*?### 关键词[^\n]*\n([\s\S]*?)(?=### 类别)"),
            ("ja", r"## 日本語[\s\S]*?### 簡単な説明[^\n]*\n([^\n]+)[\s\S]*?### キーワード[^\n]*\n([\s\S]*?)(?=### カテゴリ)"),
            ("ru", r"## Русский[\s\S]*?### Краткое описание[^\n]*\n([^\n]+)[\s\S]*?### Ключевые слова[^\n]*\n([\s\S]*?)(?=### Категория)"),
        )
        for code, pattern in section_specs:
            match = re.search(pattern, listing_text)
            if not match:
                findings.append(f"STORE_LISTING.md: Struktur für Sprache '{code}' unvollständig.")
                continue
            short_desc = match.group(1).strip()
            kws = _extract_numbered_keywords(match.group(2))
            if len(short_desc) > 100 or len(short_desc) == 0:
                findings.append(f"STORE_LISTING.md ({code}): Kurzbeschreibung ungültige Länge ({len(short_desc)} Zeichen).")
            else:
                passed.append(f"STORE_LISTING.md ({code}): Kurzbeschreibung ({len(short_desc)}/100 Zeichen) OK")

            if len(kws) != 7:
                findings.append(f"STORE_LISTING.md ({code}): Erwartet 7 nummerierte Keywords, gefunden: {len(kws)}.")
            else:
                bad_kw = [kw for kw in kws if len(kw) > 30 or _contains_forbidden_trademark(kw)]
                if bad_kw:
                    findings.append(f"STORE_LISTING.md ({code}): Ungültige Keywords (Länge/Marke): {bad_kw}")
                else:
                    passed.append(f"STORE_LISTING.md ({code}): 7/7 Keywords Richtlinie 10.1.3 konform")

    # 6. Einzel-Staging-Listings unter releases/windowsstore/store_listing_<lang>.md
    for code in TIER2_LANG_CODES:
        staged_file = project_root / "releases" / "windowsstore" / f"store_listing_{code}.md"
        if not staged_file.is_file():
            findings.append(f"Staging-Listing fehlt: releases/windowsstore/store_listing_{code}.md")
            continue
        staged_text = staged_file.read_text(encoding="utf-8")
        hit_staged = _contains_forbidden_trademark(staged_text)
        if hit_staged:
            findings.append(f"store_listing_{code}.md enthält Fremdmarke '{hit_staged}' (Richtlinie 10.1.3).")
            continue
        staged_kws = _extract_numbered_keywords(staged_text)
        if len(staged_kws) != 7:
            findings.append(f"store_listing_{code}.md: Erwartet 7 nummerierte Keywords, gefunden: {len(staged_kws)}.")
            continue
        if isinstance(pkg_data, dict) and staged_kws != pkg_data.get(f"keywords_{code}"):
            findings.append(f"store_listing_{code}.md: Keywords stimmen nicht mit store_package.json keywords_{code} überein.")
            continue
        passed.append(f"releases/windowsstore/store_listing_{code}.md: Vorhanden, 7 Keywords synchron & Policy 10.1.3 OK")

    # 7. Pflichtdokumente & Lokale-Nutzerpfad-Hygiene
    doc_paths = (
        "WINDOWS_STORE_PREP.md",
        "PRIVACY_POLICY.md",
        "releases/windowsstore/BUILD.md",
        "releases/windowsstore/WACK_PROTOCOL.md",
    )
    for rel_doc in doc_paths:
        dpath = project_root / rel_doc
        if not dpath.is_file() or dpath.stat().st_size < 120:
            findings.append(f"Store-Dokument fehlt oder ist zu kurz: {rel_doc}")
            continue
        dtext = dpath.read_text(encoding="utf-8")
        path_hits = USER_PATH_RE.findall(dtext)
        if path_hits:
            findings.append(f"{rel_doc}: Enthält lokale Benutzerpfade: {path_hits}")
        else:
            passed.append(f"{rel_doc}: Vorhanden und frei von lokalen Benutzerpfaden")

    return passed, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Windows Store Readiness Checker für SQLite Viewer Pro")
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON ausgeben")
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help="Optionales Projektroot")
    args = parser.parse_args(argv)

    passed, findings = check_store_readiness(args.root.resolve())

    if args.json:
        print(
            json.dumps(
                {
                    "status": "PASS" if not findings else "FAIL",
                    "passed_count": len(passed),
                    "finding_count": len(findings),
                    "passed": passed,
                    "findings": findings,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(f"=== SQLite Viewer Pro — Windows Store Readiness ({len(passed)} PASS, {len(findings)} FAIL) ===")
        for item in passed:
            print(f"  [PASS] {item}")
        for err in findings:
            print(f"  [FAIL] {err}")

    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())

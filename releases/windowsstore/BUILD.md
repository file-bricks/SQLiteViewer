# SQLite Viewer Pro — Windows Store Build-Anleitung

Stand: 2026-11-14 · Paketversion: `2.1.0.0` (eingefroren analog `APP_VERSION = "2.1.0"`) · Store-ID: `9P6H501XB8JT`

## Voraussetzungen

1. Python 3.10+ mit Tkinter (Standardbibliothek, 0 externe Runtime-Abhängigkeiten)
2. PyInstaller (`pip install -r requirements-dev.txt`)
3. Windows 10/11 SDK (`makeappx.exe`, `makepri.exe`, `signtool.exe`, `appcert.exe`)
4. Kanonischer Arbeitsort (Plan D): lokaler Git-Checkout `<REPO_ROOT>`

## Schritt 0: Automatisierter Store-Readiness- & Icon-Preflight

Vor jedem Packaging-Lauf die hermetischen Preflight-Gates im Repository-Root ausführen:

```powershell
python scripts/check_store_readiness.py
python -B -m pytest -q
```

Im zentralen `.SOFTWARE`-Root zusätzlich das Icon-Konsistenz-Gate prüfen:

```powershell
python _STORE/icon_consistency_check.py "<REPO_ROOT>"
```

## Schritt 1: Store-Screenshots optional aktualisieren (lokal, git-ignoriert)

```powershell
python _WARTUNG/generate_store_screenshots.py
```

Erzeugt lokal (nicht in Git versioniert):
- `releases/windowsstore/screenshots/data-browser.png`
- `releases/windowsstore/screenshots/schema-view.png`
- `releases/windowsstore/screenshots/sql-editor.png`
- `README/screenshots/main.png` (source-kontrollierter GitHub-Screenshot)

## Schritt 2: Standalone-EXE mit PyInstaller erzeugen

```powershell
pyinstaller SQLiteViewer.spec --noconfirm
```

Prüfpunkte:
- `dist/SQLiteViewer.exe` startet fensterlos (`console=False`, `RunAsInvoker`)
- Gebündelte Ressourcen: `locales/translations.json` (6 Sprachen) und `SQLiteViewer.ico` (Multi-Size 16..256 px)

## Schritt 3: MSIX-Paket bauen

1. Staging-Manifest `store_package/SQLite Viewer Pro/AppxManifest.xml` (`Identity Name="Geiger.SQLiteViewerPro"`, `Publisher="CN=52596601-BAB4-4F3F-B182-E8F3F273B202"`, `Version="2.1.0.0"`, `ProcessorArchitecture="x64"`) und `releases/windowsstore/store_settings.json` verwenden.
2. `resources.pri` für alle 6 Tier-2-Sprachen (`de-DE`, `en-US`, `es-ES`, `zh-CN`, `ja-JP`, `ru-RU`) via `makepri.exe` erzeugen.
3. MSIX via `makeappx.exe pack` im ignorierten Staging-Pfad `_WARTUNG/msix_staging/` bauen (Ausgabe lokal unter `releases/windowsstore/v2.1.0/SQLiteViewerPro-2.1.0.0.msix`).

## Schritt 4: Pretest & WACK-Zertifizierungslauf

- Automatisierten Pretest (`_STORE/msstore_pretest.ps1`) gegen `dist/SQLiteViewer.exe` ausführen (inkl. Start aus `C:\Windows\System32` zur Prüfung der CWD-Unabhängigkeit).
- Erhöhten Windows App Certification Kit Lauf (`_STORE/msstore_wack.ps1`) durch den Maintainer ausführen und Ergebnis in `releases/windowsstore/WACK_PROTOCOL.md` protokollieren.

## Schritt 5: Microsoft Partner Center Einreichung (Manuelles Owner-Gate)

- **Store-ID:** `9P6H501XB8JT` (`SQLite Viewer Pro`)
- **Preismodell:** Kostenlos (`free`) / Open Source MIT
- **Sprach-Listings (6 Tier-2-Sprachen, Richtlinie 10.1.3 geprüft):**
  - `releases/windowsstore/store_listing_de.md` (`de-DE`)
  - `releases/windowsstore/store_listing_en.md` (`en-US`)
  - `releases/windowsstore/store_listing_es.md` (`es-ES`)
  - `releases/windowsstore/store_listing_zh.md` (`zh-CN`)
  - `releases/windowsstore/store_listing_ja.md` (`ja-JP`)
  - `releases/windowsstore/store_listing_ru.md` (`ru-RU`)
- **WICHTIG:** Keine automatische Live-Einreichung durch Agenten; Upload und Zertifizierungsfreigabe erfolgen ausschließlich manuell durch den Kontoinhaber im Microsoft Partner Center.

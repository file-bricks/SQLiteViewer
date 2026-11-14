# SQLite Viewer Pro — Windows Store Test- & WACK-Protokoll

Stand: 2026-11-14 · Paketversion: `2.1.0.0` · Store-ID: `9P6H501XB8JT` · Identity: `Geiger.SQLiteViewerPro`

## Ziel

Dieses Protokoll dokumentiert den technischen Vorprüfungs-, Packaging- und WACK-Status von **SQLite Viewer Pro** für den Microsoft Store Kanal (`9P6H501XB8JT`) unter Wahrung der Policy-P-006 Tier-2 6-Sprachen-Parität und der Microsoft Partner Center Richtlinie 10.1.3.

## Geprüfte Release- & Store-Artefakte

| Artefakt | Pfad | Prüfstatus |
|---|---|---|
| Store-Paketkonfiguration | `store_package.json` | JSON valide, Version `2.1.0.0`, 6 Tier-2-Sprachen, je 7 Keywords (`<= 30` Zeichen) |
| Staging-Konfiguration | `releases/windowsstore/store_settings.json` | Synchronisiert auf `2.1.0.0`, `Geiger.SQLiteViewerPro`, `SQLiteViewer.exe` |
| MSIX-Manifest | `store_package/SQLite Viewer Pro/AppxManifest.xml` | Valides XML, `ProcessorArchitecture="x64"`, `runFullTrust`, `.db/.sqlite/.sqlite3`, Alias `sqliteviewer.exe`, 6 `<Resource Language="..."/>` |
| Kachel- & Logo-Assets | `store_assets/` & `store_package/SQLite Viewer Pro/icons/` | `44x44`, `50x50` (`StoreLogo.png`), `150x150`, `310x150`, `310x310` + 42 `targetsize`-Varianten konsistent zu `SQLiteViewer.ico` |
| Sprach-Listings (6 Sprachen) | `STORE_LISTING.md` & `releases/windowsstore/store_listing_{de,en,es,zh,ja,ru}.md` | Kurzbeschreibungen `<= 100` Zeichen, je 7 Keywords ohne Drittmarken (Richtlinie 10.1.3) |
| Datenschutzerklärung | `https://github.com/file-bricks/SQLiteViewer/blob/master/PRIVACY_POLICY.md` | Öffentlich erreichbar (Zero Network Egress, 100 % lokal) |
| Support-Kanal | `https://github.com/file-bricks/SQLiteViewer/issues` | Öffentlich erreichbar |

## Automatisierte Preflight-Gates (2026-11-14)

Ausgeführt im kanonischen Plan-D-Checkout `<REPO_ROOT>`:

```powershell
python scripts/check_store_readiness.py
python -B tests/source_platform_smoke.py
python -B -m pytest -q
```

Ergebnis:
- **Store-Readiness-Linter (`scripts/check_store_readiness.py`):** 0 Findings, 100 % PASS über Manifest, 6-Sprachen-Listings, Policy 10.1.3 Keywords, PNG-/ICO-Dimensionen und Pfad-Hygiene.
- **Icon-Konsistenz-Gate (`icon_consistency_check.py`):** PASS (`SQLiteViewer.ico` 16..256 px konsistent zu `Square310x310Logo.png` und `Wide310x150Logo.png`).
- **Pre-Submission-Laufzeitprüfung (`msstore_pretest.ps1`):** 10 PASS / 0 FAIL / 0 WARN; CWD-Unabhängigkeit aus `C:\Windows\System32` verifiziert; Einreichung `2.1.0.0` (`SQLiteViewerPro-2.1.0.0.msix`, Submission `1152921505702275474`) dokumentiert.

## Offenes Maintainer-Gate für Folge-Releases

Bei künftigen Binär-Neubauten ist vor einer neuen Partner-Center-Einreichung der erhöhte WACK-Paketlauf (`appcert.exe` / `_STORE/msstore_wack.ps1`) mit Administratorrechten gegen das lokal gebaute `.msix`-Artefakt auszuführen:

```powershell
Start-Process powershell -Verb RunAs -ArgumentList '-File "<SOFTWARE_ROOT>\_STORE\msstore_wack.ps1" -MsixPath "<REPO_ROOT>\releases\windowsstore\v2.1.0\SQLiteViewerPro-2.1.0.0.msix"'
```

Binäre `.msix`- und `.exe`-Artefakte verbleiben gemäß Repository-Hygiene lokal ignoriert außerhalb des öffentlichen Git-Baums.

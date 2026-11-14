# Windows Store Vorbereitung & Release-Readiness — SQLite Viewer Pro

**Stand:** 2026-11-14  
**App-Name:** SQLite Viewer Pro  
**Package Identity:** `Geiger.SQLiteViewerPro`  
**Microsoft Store ID:** `9P6H501XB8JT`  
**Publisher:** `CN=52596601-BAB4-4F3F-B182-E8F3F273B202` (`Geiger`)  
**Paketversion:** `2.1.0.0` (gekoppelt an eingefrorene App-Version `2.1.0`)  
**Kategorie:** Developer Tools · **Altersfreigabe:** IARC `3+` · **Lizenz:** MIT

---

## 1. Architektur- & Sicherheitsprofil für den Microsoft Store

- **Unprivilegierter Desktop-Betrieb (`RunAsInvoker`):** Keine UAC-Erhöhung, keine Registry-Manipulation außerhalb der deklarativen MSIX-Dateiverknüpfungen.
- **Zero Network Egress (`INV-LOCAL-01`):** 100 % lokale Ausführung mit der Python-Standardbibliothek (`sqlite3`, `tkinter`). Keine Telemetrie, kein Cloud-Zwang, keine externen Pip-Laufzeitabhängigkeiten.
- **Deklarative Windows-Integration (`AppxManifest.xml`):**
  - `ProcessorArchitecture="x64"`, `Windows.FullTrustApplication` (`SQLiteViewer.exe`)
  - Dateityp-Verknüpfungen (`uap:FileTypeAssociation`): `.db`, `.sqlite`, `.sqlite3`
  - App Execution Alias (`uap3:AppExecutionAlias`): `sqliteviewer.exe`
  - Ressourcen-Deklaration für alle 6 Tier-2-Sprachen (`de-DE`, `en-US`, `es-ES`, `zh-CN`, `ja-JP`, `ru-RU`)

---

## 2. Tier-2 6-Sprachen-Abdeckung & Richtlinie 10.1.3

Alle Metadaten und Store-Texte sind synchron über **Deutsch (`de-DE`)**, **Englisch (`en-US`)**, **Spanisch (`es-ES`)**, **Vereinfachtes Chinesisch (`zh-CN`)**, **Japanisch (`ja-JP`)** und **Russisch (`ru-RU`)** gepflegt:

| Quelle | Zweck | Richtlinien-Status |
|---|---|---|
| [`store_package.json`](store_package.json) | Kanonische Paket- & Sprachmetadaten im Repo-Root | 6 Kurzbeschreibungen (`<= 100` Zeichen), je 7 Keywords (`<= 30` Zeichen, null Drittmarken) |
| [`releases/windowsstore/store_settings.json`](releases/windowsstore/store_settings.json) | WinStorePackager- & Build-Konfiguration | 100 % synchron zu `store_package.json` (`2.1.0.0`, `Geiger.SQLiteViewerPro`) |
| [`STORE_LISTING.md`](STORE_LISTING.md) | Gesamtdokumentation aller 6 Store-Listings | Frei von Drittmarken-Vergleichen im Store-Text, exakt 7 Keywords je Sprache |
| `releases/windowsstore/store_listing_{de,en,es,zh,ja,ru}.md` | Einzelvorlagen für Copy-&-Paste im Partner Center | Vollständig vorhanden für alle 6 Zielsprachen |

---

## 3. Icon- & Kachel-Inventar

Alle Kachel- und Logo-Assets sind aus derselben visuellen Quelle (`store_assets/Square310x310Logo.png`) abgeleitet und bestehen das zentrale Icon-Konsistenz-Gate (`icon_consistency_check.py`):

- `SQLiteViewer.ico` (Multi-Frame Desktop-/EXE-Icon bis `256x256` px)
- `store_assets/StoreLogo.png` & `store_assets/Square50x50Logo.png` & `releases/windowsstore/StoreLogo.png` (`50x50` px)
- `store_assets/Square44x44Logo.png` (`44x44` px) inkl. 42 `targetsize-{16..256}`-Varianten (`plated`, `unplated`, `lightunplated`)
- `store_assets/Square150x150Logo.png` (`150x150` px)
- `store_assets/Wide310x150Logo.png` (`310x150` px)
- `store_assets/Square310x310Logo.png` (`310x310` px)
- Paket-Spiegel unter `store_package/SQLite Viewer Pro/icons/icon_{44x44,50x50,150x150,310x150,310x310}.png`

---

## 4. Automatisierte Vorprüfung (Preflight)

Die Einhaltung sämtlicher Manifest-, Asset-, Sprach- und Richtlinienvorgaben wird ohne externe Abhängigkeiten geprüft über:

```bash
python scripts/check_store_readiness.py
python -B -m pytest tests/test_store_materials.py -v
```

Build-Schritte und WACK-Nachweisführung sind in [`releases/windowsstore/BUILD.md`](releases/windowsstore/BUILD.md) und [`releases/windowsstore/WACK_PROTOCOL.md`](releases/windowsstore/WACK_PROTOCOL.md) dokumentiert. Partner-Center-Uploads bleiben ein explizites manuelles Maintainer-Gate.

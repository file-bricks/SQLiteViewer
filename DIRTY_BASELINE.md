# Dirty-Baseline – SQLiteViewer OneDrive-Arbeitsbaum

Stand: 2026-07-22. Baseline vor TASKSOLVER #971/#972/#974: `master` und
`origin/master` zeigen auf `81ee8091b7dfe502264a91fa1ce5dbd5abc57386`.
Der autoritative, saubere Plan-D-Clone liegt unter
`C:\\_Local_DEV\\repos\\SQLiteViewer`; er enthält keine der untenstehenden
OneDrive-Änderungen. Keine Datei wurde übernommen, verschoben, archiviert,
gelöscht, committed oder im Clone verwendet.

## Entscheidung je Datei

Alle Einträge sind **separat klären**: Es gibt keinen belastbaren Auftrag,
keinen verfolgbaren Commit und keine passende bestätigte Produktreferenz, die
eine Übernahme oder ein Ignorieren per `.gitignore` autorisieren würde.

| Datei | Git-Status | SHA-256 | Befund | Entscheidung |
|---|---|---|---|---|
| `START.bat` | modified | `84b7d411693e6e1d6d99aaf994aff1e4c2892781101d658dbdbbe5be350740e2` | getrackt, History bis `ee415cc`; normaler Diff leer (nur Arbeitsbaum-/EOL-Zustand feststellbar) | separat klären |
| `build_exe.bat` | modified | `2cfa95f66059e088e10e88c410324b1340e2fdf248a86f7fb283cb73143bfe0d` | getrackt, History bis `ee415cc`; normaler Diff leer (nur Arbeitsbaum-/EOL-Zustand feststellbar) | separat klären |
| `assets/android-icon-background.png` | untracked | `079830d65fb6cda297c7bcc2c983097494623efdd9b5491e7ccc43548284243` | 512×512, keine Git-Historie | separat klären |
| `assets/android-icon-foreground.png` | untracked | `7bcb6e252e6bc8b026ce9530211712b50cc35e7f61fd3fbe95b3a07a9a52725e` | 512×512, keine Git-Historie | separat klären |
| `assets/android-icon-monochrome.png` | untracked | `bc0f9936b0bd419bc8147384ad76a9490f02207da6f09df6a68856a99ca7e831` | 512×512, identisch zu `assets/icon.png` und `assets/splash-icon.png`, keine Git-Historie | separat klären |
| `assets/favicon.png` | untracked | `dc38199db497e8d28fe9dc960509f3a6875b596ec44c9c094f287133fcc72a58` | 32×32, identisch zu den Companion-Favicons, keine Git-Historie | separat klären |
| `assets/icon.png` | untracked | `bc0f9936b0bd419bc8147384ad76a9490f02207da6f09df6a68856a99ca7e831` | 512×512, identisch zu monochrome/splash, keine Git-Historie | separat klären |
| `assets/splash-icon.png` | untracked | `bc0f9936b0bd419bc8147384ad76a9490f02207da6f09df6a68856a99ca7e831` | 512×512, identisch zu monochrome/icon, keine Git-Historie | separat klären |
| `web_companion/apple-touch-icon-180.png` | untracked | `9ae25897d449fd1e1c73fb5291ebaefa6b332220689c237d89bda1e6814b2ed7` | 180×180, identisch zu zwei weiteren Apple-Touch-Varianten; HTML referenziert stattdessen `icons/sqliteviewer-companion-180.png` | separat klären |
| `web_companion/apple-touch-icon.png` | untracked | `9ae25897d449fd1e1c73fb5291ebaefa6b332220689c237d89bda1e6814b2ed7` | 180×180, keine direkte Produktreferenz | separat klären |
| `web_companion/favicon.png` | untracked | `dc38199db497e8d28fe9dc960509f3a6875b596ec44c9c094f287133fcc72a58` | 32×32, keine direkte Produktreferenz | separat klären |
| `web_companion/icons/apple-touch-icon-180.png` | untracked | `9ae25897d449fd1e1c73fb5291ebaefa6b332220689c237d89bda1e6814b2ed7` | 180×180, keine direkte Produktreferenz | separat klären |
| `web_companion/icons/apple-touch-icon.png` | untracked | `9ae25897d449fd1e1c73fb5291ebaefa6b332220689c237d89bda1e6814b2ed7` | 180×180, keine direkte Produktreferenz | separat klären |
| `web_companion/icons/favicon.png` | untracked | `dc38199db497e8d28fe9dc960509f3a6875b596ec44c9c094f287133fcc72a58` | 32×32, keine direkte Produktreferenz | separat klären |

`git check-ignore` meldet für alle Tabellenzeilen „nicht ignoriert“. Der
Folgeauftrag muss Herkunft und gewünschten Zielpfad bestätigen, bevor eine
Übernahme, Archivierung oder Ignore-Regel zulässig ist.

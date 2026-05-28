from __future__ import annotations

import sqlite3
import sys
import tempfile
import time
import ctypes
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from SQLiteViewer import SqlViewer


SCREENSHOTS = (
    ("data-browser.png", "Datenansicht mit geöffneter Beispieldatenbank"),
    ("schema-view.png", "Schema-Ansicht der Beispieldatenbank"),
    ("sql-editor.png", "SQL-Editor mit ausgeführter Beispielabfrage"),
)


def create_demo_database(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(target) as conn:
        conn.executescript(
            """
            DROP TABLE IF EXISTS projects;
            DROP TABLE IF EXISTS notes;

            CREATE TABLE projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                owner TEXT NOT NULL,
                status TEXT NOT NULL,
                rows_estimate INTEGER NOT NULL
            );

            CREATE TABLE notes (
                id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            );
            """
        )
        conn.executemany(
            "INSERT INTO projects (name, owner, status, rows_estimate) VALUES (?, ?, ?, ?)",
            [
                ("Customer Analytics", "Lena", "aktiv", 18420),
                ("Billing Snapshot", "Mika", "review", 6120),
                ("Sandbox Import", "Noah", "archiviert", 240),
            ],
        )
        conn.executemany(
            "INSERT INTO notes (project_id, title, body) VALUES (?, ?, ?)",
            [
                (1, "Export", "JSON-Export für Companion prüfen"),
                (2, "Filter", "CSV-Export gegen Demo-Daten getestet"),
                (3, "Archiv", "Read-only-Sichtung ohne Änderungen"),
            ],
        )


def wait_for_ui(app: SqlViewer, pause: float = 0.3) -> None:
    app.update_idletasks()
    app.update()
    time.sleep(pause)
    app.update_idletasks()
    app.update()


def capture_window(app: SqlViewer, target: Path) -> None:
    try:
        from PIL import Image, ImageGrab
        import win32gui
        import win32ui
    except ImportError as exc:
        raise RuntimeError(
            "Store screenshot generation requires Pillow and pywin32 on Windows."
        ) from exc

    wait_for_ui(app)
    hwnd = app.winfo_id()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = max(1, right - left)
    height = max(1, bottom - top)

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)

    try:
        result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0x00000002)
        if result == 1:
            bmp_info = bitmap.GetInfo()
            bmp_bytes = bitmap.GetBitmapBits(True)
            image = Image.frombuffer(
                "RGB",
                (bmp_info["bmWidth"], bmp_info["bmHeight"]),
                bmp_bytes,
                "raw",
                "BGRX",
                0,
                1,
            )
        else:
            image = ImageGrab.grab(bbox=(left, top, right, bottom))
    finally:
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, "PNG")


def render_data_browser(app: SqlViewer) -> None:
    app.notebook.select(app.data_frame)
    app.table_var.set("projects")
    app.load_selected_table()


def render_schema_view(app: SqlViewer) -> None:
    app.notebook.select(app.schema_frame)
    app.schema_table_var.set("projects")
    app._load_schema()


def render_sql_editor(app: SqlViewer) -> None:
    app.notebook.select(app.sql_frame)
    app.sql_text.delete("1.0", "end")
    app.sql_text.insert(
        "1.0",
        (
            "SELECT name, owner, rows_estimate\n"
            "FROM projects\n"
            "WHERE status != 'archiviert'\n"
            "ORDER BY rows_estimate DESC;"
        ),
    )
    app.execute_sql()


def write_manifest(output_dir: Path) -> None:
    lines = ["# Store-Screenshots", ""]
    for name, caption in SCREENSHOTS:
        lines.append(f"- `{name}` - {caption}")
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_store_screenshots(output_dir: Path | None = None) -> list[Path]:
    output_dir = output_dir or (PROJECT_ROOT / "releases" / "windowsstore" / "screenshots")
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="sqliteviewer-store-shots-") as temp_dir:
        demo_db = Path(temp_dir) / "sqliteviewer-demo.sqlite"
        create_demo_database(demo_db)

        app = SqlViewer()
        app.geometry("1460x920+40+40")
        app.update_idletasks()
        app.update()
        app.open_db_path(str(demo_db))
        wait_for_ui(app, pause=0.5)

        targets = []
        try:
            render_data_browser(app)
            data_target = output_dir / SCREENSHOTS[0][0]
            capture_window(app, data_target)
            targets.append(data_target)

            render_schema_view(app)
            schema_target = output_dir / SCREENSHOTS[1][0]
            capture_window(app, schema_target)
            targets.append(schema_target)

            render_sql_editor(app)
            sql_target = output_dir / SCREENSHOTS[2][0]
            capture_window(app, sql_target)
            targets.append(sql_target)
        finally:
            app._on_close()

    readme_main = PROJECT_ROOT / "README" / "screenshots" / "main.png"
    readme_main.parent.mkdir(parents=True, exist_ok=True)
    readme_main.write_bytes((output_dir / SCREENSHOTS[0][0]).read_bytes())
    write_manifest(output_dir)
    return targets


def main() -> int:
    targets = generate_store_screenshots()
    for target in targets:
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

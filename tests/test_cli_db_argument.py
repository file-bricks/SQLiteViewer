# -*- coding: utf-8 -*-
"""Belegt, dass eine per Kommandozeile uebergebene Datenbank geoeffnet wird.

Hintergrund: Das Store-Paket deklarierte keine Dateizuordnung. Damit ein
Doppelklick auf eine .db-Datei funktioniert, braucht es beides - den
Manifest-Eintrag UND die Auswertung des Arguments. Letztere war hier bereits
vorhanden; dieser Test haelt sie fest, damit sie nicht unbemerkt wegfaellt.

Bewusst ohne GUI-Instanziierung: SqlViewer() blockiert in einer Umgebung ohne
Anzeige, statt zu scheitern - ein Test, der das versucht, haengt bis zum
Timeout, statt eine Aussage zu treffen.
"""
from __future__ import annotations

import ast
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "SQLiteViewer.py")


def _source():
    with open(SOURCE, encoding="utf-8") as f:
        return f.read()


def test_entrypoint_forwards_first_argument():
    """Der Einstiegspunkt muss argv[1] an open_db_path weiterreichen."""
    src = _source()
    assert "len(sys.argv) > 1" in src, "Kommandozeilenargument wird nicht geprueft"
    assert "open_db_path(sys.argv[1])" in src, "argv[1] wird nicht an open_db_path gereicht"


def test_open_db_path_exists_and_takes_a_path():
    """open_db_path muss existieren und genau einen Pfad entgegennehmen."""
    tree = ast.parse(_source())
    found = [n for n in ast.walk(tree)
             if isinstance(n, ast.FunctionDef) and n.name == "open_db_path"]
    assert found, "open_db_path nicht gefunden"
    args = [a.arg for a in found[0].args.args]
    assert args[0] == "self" and len(args) >= 2, (
        "open_db_path nimmt keinen Pfad entgegen: %s" % args)


def test_declared_extensions_match_the_file_dialog():
    """Die im Store-Paket deklarierten Endungen muessen denen des Dialogs entsprechen.

    Sonst bietet Windows die App fuer Dateien an, die sie selbst nicht anbietet.
    """
    import json
    with open(os.path.join(ROOT, "store_package.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    declared = {e.lower() for e in (cfg.get("file_types") or {}).get("extensions", [])}
    assert declared, "store_package.json deklariert keine Dateitypen"
    src = _source()
    for ext in declared:
        assert "*%s" % ext in src, (
            "%s ist im Manifest deklariert, kommt im Dateidialog aber nicht vor" % ext)


def test_sqlite_roundtrip_is_possible(tmp_path):
    """Sicherstellen, dass die Testumgebung ueberhaupt SQLite schreiben kann."""
    p = tmp_path / "probe.db"
    con = sqlite3.connect(str(p))
    con.execute("CREATE TABLE t (a INTEGER)")
    con.commit()
    con.close()
    assert p.exists() and p.stat().st_size > 0

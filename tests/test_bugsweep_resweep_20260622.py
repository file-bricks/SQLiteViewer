# -*- coding: utf-8 -*-
"""Regressionstests — SQLiteViewer Desktop-Re-Sweep 2026-06-22 (Bugsweep-Loop-Lauf 23).

_serialize_export_value ist ohne Tk-Instanz aufrufbar -> echter Test; Rest statisch.
Red-on-revert: SQLV_SRC -> PRE-Backup-Verzeichnis.

  B-06 _serialize: NaN/Inf -> String (sonst invalides JSON).
  B-04 export_csv: BLOB/bytes base64-kodieren (statt b'...'-Rohliteral).
  A-BUG-4 limit_var.get(): auch tk.TclError fangen (leere/ungueltige Spinbox).
  B-09 translator._save_translations: OSError-Guard (read-only FS).
"""
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_SRC = Path(os.environ.get("SQLV_SRC", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SV = (_SRC / "SQLiteViewer.py").read_text(encoding="utf-8")
TR = (_SRC / "translator.py").read_text(encoding="utf-8")


def has(n, src=SV):
    return n in src


# --- echter Test (B-06) ---
def test_b06_serialize_non_finite_floats():
    import SQLiteViewer as M

    class _Dummy:
        pass

    fn = M.SqlViewer._serialize_export_value
    d = _Dummy()
    assert fn(d, float("nan")) == "nan"
    assert fn(d, float("inf")) == "inf"
    assert fn(d, 3.5) == 3.5
    assert fn(d, None) is None
    # base64-BLOB weiterhin korrekt
    blob = fn(d, b"\x00\xff")
    assert isinstance(blob, dict) and blob["type"] == "blob"
    # nach Serialisierung gueltiges JSON
    json.dumps(fn(d, float("nan")))  # darf nicht werfen (kein NaN-Literal)


# --- statische Assertions (red-on-revert) ---
def test_b04_export_csv_blob_base64():
    assert has('b64encode(v).decode("ascii") if isinstance(v, bytes)'), "B-04 CSV-BLOB-base64 fehlt"


def test_a4_limit_var_tclerror():
    assert has("ValueError, TypeError, tk.TclError"), "A-BUG-4 tk.TclError-Guard fehlt"
    assert not has("        except (ValueError, TypeError):\n"), "A-BUG-4 alter except ohne TclError noch da"


def test_b06_serialize_guard_static():
    assert has("math.isfinite(value)"), "B-06 NaN/Inf-Guard fehlt"


def test_b09_translator_save_guard():
    assert has("except OSError:", TR), "B-09 translator OSError-Guard fehlt"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

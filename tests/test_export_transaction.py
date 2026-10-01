import csv
import json
import os
import sqlite3
from types import SimpleNamespace

import pytest
import SQLiteViewer as module
import export_atomic


@pytest.fixture
def viewer(tmp_path, monkeypatch):
    source = tmp_path / 'source.sqlite'
    db = sqlite3.connect(source)
    db.execute('create table items(name text)')
    db.execute("insert into items values ('Grüße')")
    db.commit()
    db.close()
    conn = sqlite3.connect(source.as_uri() + '?mode=ro', uri=True)
    messages = []
    fake = SimpleNamespace(db_path=str(source), conn=conn, current_columns=['name', 'blob'],
                           current_data=[('Grüße', b'AB')], export_context={'view': 'table', 'table': 'items'},
                           table_var=SimpleNamespace(get=lambda: 'items'), _set_status=lambda *_: None)
    fake._build_export_payload = lambda: module.SqlViewer._build_export_payload(fake)
    for name in ('showerror', 'showinfo', 'showwarning'):
        monkeypatch.setattr(module.messagebox, name, lambda *args, name=name: messages.append((name, args)))
    yield fake, source, messages
    conn.close()


def run_export(viewer, kind, destination, monkeypatch, dialog=None):
    monkeypatch.setattr(module.filedialog, 'asksaveasfilename', dialog or (lambda **_: str(destination)))
    getattr(module.SqlViewer, 'export_' + kind)(viewer)


@pytest.mark.parametrize('kind', ['csv', 'json'])
@pytest.mark.parametrize('alias', ['direct', 'hardlink', 'wal', 'shm', 'journal'])
def test_export_rejects_source_and_sidecars(viewer, kind, alias, monkeypatch):
    fake, source, messages = viewer
    before = source.read_bytes()
    target = source
    if alias == 'hardlink':
        target = source.with_name('alias.out')
        os.link(source, target)
    elif alias != 'direct':
        target = source.with_name(source.name + '-' + alias)
        target.write_bytes(b'protected sidecar')
    target_before = target.read_bytes()
    run_export(fake, kind, target, monkeypatch)
    assert source.read_bytes() == before
    assert target.read_bytes() == target_before
    assert [m[0] for m in messages] == ['showerror']


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_attached_database_protected(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    attached = tmp_path / 'attached.sqlite'
    db = sqlite3.connect(attached)
    db.execute('create table extra(id integer)')
    db.close()
    fake.conn.execute('ATTACH DATABASE ? AS extra', (str(attached),))
    before = attached.read_bytes()
    run_export(fake, kind, attached, monkeypatch)
    assert attached.read_bytes() == before
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_modal_database_change_keeps_original_protected(viewer, kind, monkeypatch):
    fake, source, messages = viewer
    before = source.read_bytes()
    def dialog(**_):
        fake.db_path = None
        fake.conn.close()
        fake.conn = None
        return str(source)
    run_export(fake, kind, source, monkeypatch, dialog)
    assert source.read_bytes() == before
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
@pytest.mark.parametrize('fault', ['fsync', 'replace', 'serialization'])
def test_failed_export_preserves_previous_output(viewer, kind, fault, tmp_path, monkeypatch):
    fake, source, messages = viewer
    target = tmp_path / ('output.' + kind)
    target.write_bytes(b'previous output')
    foreign = tmp_path / '.sqliteviewer-export-foreign.tmp'
    foreign.write_bytes(b'foreign')
    def fail(*_, **__):
        raise OSError('injected failure')
    if fault == 'serialization':
        class Broken:
            def __str__(self):
                raise ValueError('invalid value')
        fake.current_data = [(Broken(), b'AB')]
    else:
        monkeypatch.setattr(export_atomic.os, 'fsync' if fault == 'fsync' else 'replace', fail)
    run_export(fake, kind, target, monkeypatch)
    assert target.read_bytes() == b'previous output'
    assert foreign.read_bytes() == b'foreign'
    assert list(tmp_path.glob('.sqliteviewer-export-*.tmp')) == [foreign]
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_export_snapshot_survives_dialog_change(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    target = tmp_path / ('output.' + kind)
    def dialog(**_):
        fake.current_columns = ['other']
        fake.current_data = [('changed',)]
        fake.db_path = 'different.sqlite'
        return str(target)
    run_export(fake, kind, target, monkeypatch, dialog)
    if kind == 'csv':
        with target.open(encoding='utf-8-sig', newline='') as handle:
            assert list(csv.reader(handle, delimiter=';')) == [['name', 'blob'], ['Grüße', 'QUI=']]
    else:
        payload = json.loads(target.read_text(encoding='utf-8'))
        assert payload['columns'] == ['name', 'blob']
        assert payload['source']['database_path'] == str(source)
        assert payload['result_rows'][0]['name'] == 'Grüße'
    assert messages[0][0] == 'showinfo'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_late_source_alias_rejected(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    target = tmp_path / 'late.out'
    before = source.read_bytes()
    original = export_atomic.os.fsync
    def replace_with_link(fd):
        original(fd)
        os.link(source, target)
    monkeypatch.setattr(export_atomic.os, 'fsync', replace_with_link)
    run_export(fake, kind, target, monkeypatch)
    assert source.read_bytes() == before
    assert target.read_bytes() == before
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_cancel_creates_nothing(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    run_export(fake, kind, '', monkeypatch)
    assert messages == []
    assert not list(tmp_path.glob('.sqliteviewer-export-*.tmp'))


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_new_attachment_during_serialization_protected(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    attached = tmp_path / 'new.sqlite'
    db = sqlite3.connect(attached)
    db.execute('create table items(id integer)')
    db.close()
    before = attached.read_bytes()
    original = export_atomic.os.fsync
    def attach(fd):
        original(fd)
        fake.conn.execute('ATTACH DATABASE ? AS newly_attached', (str(attached),))
    monkeypatch.setattr(export_atomic.os, 'fsync', attach)
    run_export(fake, kind, attached, monkeypatch)
    assert attached.read_bytes() == before
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_closed_connection_does_not_bypass_protection(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    fake.conn.close()
    target = tmp_path / 'output'
    target.write_bytes(b'previous')
    run_export(fake, kind, target, monkeypatch)
    assert target.read_bytes() == b'previous'
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_missing_sidecar_is_reserved(viewer, kind, monkeypatch):
    fake, source, messages = viewer
    target = source.with_name(source.name + '-wal')
    assert not target.exists()
    run_export(fake, kind, target, monkeypatch)
    assert not target.exists()
    assert messages[0][0] == 'showerror'


@pytest.mark.parametrize('kind', ['csv', 'json'])
def test_identity_permission_failure_preserves_output(viewer, kind, tmp_path, monkeypatch):
    fake, source, messages = viewer
    target = tmp_path / 'output'
    target.write_bytes(b'previous')
    def denied(*_):
        raise PermissionError('identity denied')
    monkeypatch.setattr(export_atomic.os.path, 'samefile', denied)
    run_export(fake, kind, target, monkeypatch)
    assert target.read_bytes() == b'previous'
    assert messages[0][0] == 'showerror'


@pytest.mark.skipif(os.name != 'nt', reason='Win32 filename normalization')
@pytest.mark.parametrize('kind', ['csv', 'json'])
@pytest.mark.parametrize('suffix', ['.', ' '])
def test_windows_sidecar_name_normalization_rejected(viewer, kind, suffix, monkeypatch):
    fake, source, messages = viewer
    reserved = source.with_name(source.name + '-wal')
    run_export(fake, kind, str(reserved) + suffix, monkeypatch)
    assert not reserved.exists()
    assert messages[0][0] == 'showerror'


def test_reserved_broken_symlink_name_is_protected(tmp_path, monkeypatch):
    source = tmp_path / 'source.sqlite'
    reserved = source.with_name(source.name + '-wal')
    # Emulate resolution of a broken link without requiring Windows symlink privilege.
    foreign = tmp_path / 'missing-foreign'
    original = export_atomic.Path.resolve
    def resolve(path, *args, **kwargs):
        return foreign if path == reserved else original(path, *args, **kwargs)
    monkeypatch.setattr(export_atomic.Path, 'resolve', resolve)
    with pytest.raises(ValueError, match='geschützte Datenbankdatei'):
        export_atomic.protect_destination(reserved, {reserved})

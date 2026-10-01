"""Failure-preserving text exports with SQLite source-file protection."""
from contextlib import contextmanager
import logging
import os
from pathlib import Path
import tempfile


def database_files(viewer):
    """Capture main and attached database names, including SQLite sidecars."""
    names = []
    if getattr(viewer, 'db_path', None):
        names.append(viewer.db_path)
    connection = getattr(viewer, 'conn', None)
    if connection is not None:
        cursor = connection.execute('PRAGMA database_list')
        try:
            names.extend(row[2] for row in cursor.fetchall() if row[2])
        finally:
            cursor.close()
    paths = set()
    for name in names:
        if name == ':memory:':
            continue
        for path in (Path(name).absolute(), Path(name).resolve()):
            paths.add(path)
            paths.update(Path(str(path) + suffix) for suffix in ('-wal', '-shm', '-journal'))
    return paths


def protect_destination(destination, sources):
    lexical_target = Path(os.path.abspath(destination))
    if os.name == 'nt' and any(
        part not in ('.', '..') and part.endswith((' ', '.'))
        for part in Path(destination).parts
    ):
        raise ValueError('Das Exportziel enthält einen mehrdeutigen Windows-Dateinamen. Bitte einen anderen Pfad wählen.')
    target = Path(destination).resolve()
    for source in sources:
        if lexical_target == Path(os.path.abspath(source)) or target == source.resolve():
            raise ValueError('Das Exportziel ist eine geschützte Datenbankdatei. Bitte einen anderen Pfad wählen.')
        try:
            same = os.path.samefile(destination, source)
        except FileNotFoundError:
            same = False
        if same:
            raise ValueError('Das Exportziel ist eine geschützte Datenbankdatei. Bitte einen anderen Pfad wählen.')


@contextmanager
def atomic_export(destination, sources, *, encoding, newline=None, refresh_sources=None):
    """Publish a complete sibling temporary file after rechecking identity."""
    destination = Path(destination).absolute()
    protect_destination(destination, sources)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding=encoding, newline=newline,
                                         dir=destination.absolute().parent,
                                         prefix='.sqliteviewer-export-', suffix='.tmp',
                                         delete=False) as handle:
            temporary = Path(handle.name)
            yield handle
            handle.flush()
            os.fsync(handle.fileno())
        if refresh_sources is not None:
            sources = sources | refresh_sources()
        protect_destination(destination, sources)
        os.replace(temporary, destination)
        temporary = None
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                logging.getLogger(__name__).warning('Cannot remove own export temporary file: %s', temporary, exc_info=True)

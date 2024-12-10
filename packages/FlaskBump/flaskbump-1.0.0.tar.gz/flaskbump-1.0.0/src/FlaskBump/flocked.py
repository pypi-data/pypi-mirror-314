import contextlib
import fcntl as fctl # I dislike 'cntl'
from pathlib import Path

from io import IOBase
from typing import Union

def open_lockfile(filepath: str | Path):
    """
    Wrapper around the `open` builtin to ensure the unique existence
    of the lockfile at `filepath`
    """

    if isinstance(filepath, str):
        filepath = Path(filepath)

    try:
        # Try creating the lock file with O_EXCL
        # O_EXCL is required to avoid sibling process race conditions of
        # multiple processes each creating their own lockfile on top of each other
        filepath.touch(exist_ok = False)
    except FileExistsError:
        # If it already exists then that's fine
        pass

    return filepath.open()

@contextlib.contextmanager
def flocked(f: Union[IOBase, int], operation: int = fctl.LOCK_EX):
    """
    Context manager for locking a file via `flock`
    """

    fctl.flock(f, operation)
    try:
        yield
    finally:
        fctl.flock(f, fctl.LOCK_UN)

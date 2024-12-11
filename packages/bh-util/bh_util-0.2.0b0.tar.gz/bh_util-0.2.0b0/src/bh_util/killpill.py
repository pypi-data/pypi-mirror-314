#!/usr/bin/env python3
from pathlib import Path

class KillPill:
    def __init__(self, path=None):
        if path is None:
            self._path = Path.home()/'die'
        else:
            self._path = Path(path)
    def path(self):
        return self._path
    def __bool__(self):
        return self._path.exists()
    def kill(self):
        self._path.touch()
    def clear(self):
        if self._path.exists():
            self._path.unlink()

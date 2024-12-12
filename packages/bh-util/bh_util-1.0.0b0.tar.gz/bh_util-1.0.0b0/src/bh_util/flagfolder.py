#!/usr/bin/env python3
from pathlib import Path
import tempfile
import time
import sys

class FlagFolder:
    def __init__(self, path):
        self._path = Path(path)
        if not self._path.exists():
            self._path.mkdir(parents=True, exist_ok=True)

    def flags(self):
        return sorted([x.name for x in self._path.glob('*')])

    def stat(self,flag):
        path = self._path/flag
        return path.exists()

    def set(self,flag):
        path = self._path/flag
        path.exists() or path.touch()

    def clear(self,flag):
        path = self._path/flag
        path.exists() and path.unlink()

    def clear_all(self):
        for path in self._path.glob('*'):
            path.unlink()


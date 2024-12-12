#!/usr/bin/env python3

import pytest

from bh_util.singletons.debug import DebugSingleton as Debug

def test_dunder_init__True_False():
    assert Debug(True)
    assert Debug()
    assert not Debug(False)
    assert not Debug()

def test_note__True(capsys):
    Debug(True).note("Hello")
    captured = capsys.readouterr()
    assert captured.err == "Hello\n"
    assert captured.out == ""

def test_note__False(capsys):
    Debug(False).note("Hello")
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""

def test_note__end(capsys):
    Debug(True)
    Debug().note("Hello", end='!')
    captured = capsys.readouterr()
    assert captured.err == "Hello!"
    assert captured.out == ""


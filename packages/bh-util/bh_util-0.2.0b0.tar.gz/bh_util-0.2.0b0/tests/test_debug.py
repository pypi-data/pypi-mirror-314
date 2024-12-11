#!/usr/bin/env python3
import sys
from pathlib import Path

import pytest

from bh_util.debug import Debug
ATTRIBNAME='_bh_debug'
@pytest.fixture()
def pill():
    try:
        del sys._bh_debug
    except AttributeError:
        pass
    pill = KillPill()
    yield KillPill()
def test_dunder_init__True_False():
    debug = Debug(True)
    assert debug
    debug = Debug(False)
    assert not debug

def test_dunder_init__True_null():
    debug = Debug(True)
    assert debug
    debug = Debug()
    assert not debug

def test_turn_on():
    debug = Debug()
    assert not debug
    debug.turn_on()
    assert debug

def test_turn_off():
    debug = Debug(True)
    assert debug
    debug.turn_off()
    assert not debug

def test_err__debug_on(capsys):
    debug = Debug(True)
    debug.err("Hello")
    captured = capsys.readouterr()
    assert captured.err == "Hello\n"
    assert captured.out == ""

def test_err__debug_on_test_end(capsys):
    debug = Debug(True)
    debug.err("Hello", end='')
    captured = capsys.readouterr()
    assert captured.err == "Hello"
    assert captured.out == ""

def test_err__debug_off(capsys):
    debug = Debug(False)
    debug.err("Hello", end='')
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""



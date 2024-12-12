#!/usr/bin/env python3

from pathlib import Path

import pytest

from bh_util.killpill import KillPill

@pytest.fixture()
def pill():
    pill = KillPill()
    yield KillPill()

def test_dunder_init__assert_default_path(pill):
    assert pill.path() == Path.home()/'die'

def test_kill_clear__boolean(pill):
    pill.clear()
    assert not pill
    pill.kill()
    assert pill
    pill.clear()
    assert not pill

def test_kill_clear__path_existance(pill):
    pill.clear()
    assert not pill.path().exists()
    pill.kill()
    assert pill.path().exists()
    pill.clear()
    assert not pill.path().exists()



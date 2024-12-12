from pathlib import Path
import tempfile
import shutil

import pytest

from bh_util.flagfolder import FlagFolder

@pytest.fixture(scope='module')
def sandbox():
    box = tempfile.mkdtemp()
    yield box
    assert Path(box).exists()
    shutil.rmtree(box)
    assert not Path(box).exists()

@pytest.fixture()
def tmp(sandbox):
    yield Path(tempfile.mkdtemp(dir=str(sandbox)))

@pytest.fixture()
def ff(tmp):
    return FlagFolder(tmp)

###########################

def test_flags__after_init(ff):
    assert ff.flags() == []

def test_flags__after_set(ff):
    ff.set('foo')
    assert ff.flags() == ['foo']

def test_flags__after_set2(ff):
    ff.set('foo')
    ff.set('bar')
    assert ff.flags() == ['bar', 'foo']

def test_clear(ff):
    ff.set('foo')
    ff.set('bar')
    ff.clear('foo')
    assert ff.flags() == ['bar']

def test_clear_all(ff):
    ff.set('foo')
    ff.set('bar')
    ff.clear_all()
    assert ff.flags() == []


def test_stat__after_init(ff):
    assert ff.stat('foo') == False
def test_stat__after_set(ff):
    ff.set('foo')
    assert ff.stat('foo') == True
def test_stat__after_clear(ff):
    ff.set('foo')
    ff.clear('foo')
    assert ff.stat('foo') == False

def test_dunder_init__can_create_deep_folder(tmp):
    path = tmp/'a/b/c'
    assert not path.exists()
    FlagFolder(path)
    assert path.exists()

def test_dunder_init__flags_are_retained(tmp):
    old =  FlagFolder(tmp)
    old.set('foo')
    new = FlagFolder(tmp)
    assert new.stat('foo')



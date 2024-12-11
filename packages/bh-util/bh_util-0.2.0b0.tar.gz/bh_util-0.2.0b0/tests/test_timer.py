#!/usr/bin/env python3
import time

import pytest

from bh_util.timer import Timer

def test_dunder_short():
    duration=0.05
    tick=0.0001
    count=5
    timer = Timer(duration=duration,count=count, tick=tick)
    acc = []
    t0 = time.time()
    while timer:
        if timer.poll():
            acc.append(timer.count())
        timer.tick()
    assert time.time()-t0 == pytest.approx(duration, rel=1e-2)
    assert acc==[4,3,2,1,0]

def test_dunder_long():
    duration=0.5
    tick=0.0001
    count=5
    timer = Timer(duration=duration,count=count, tick=tick)
    acc = []
    t0 = time.time()
    while timer:
        if timer.poll():
            acc.append(timer.count())
        timer.tick()
    assert time.time()-t0 == pytest.approx(duration, rel=1e-2)
    assert acc==[4,3,2,1,0]

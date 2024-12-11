#!/usr/bin/env python3
import time

class Timer:
    def __repr__(self):
        d = int(self._duration)
        p = int(self.percent()*100)
        c = self.count()
        return f'<Timer({d}):{p}%:count={c}>'

    def poll(self):
        c = self.count()
        if not c in self._counts:
            self._counts.append(c)
            return True
        return False

    def __init__(self, duration, count, tick):
        self._duration = duration
        self._count = count
        self._tick = tick
        self._counts = []
        self._t0 = time.time()
        self._deadline = self._t0 + duration

    def remaining(self):
        return self._deadline - time.time()

    def tick(self):
        time.sleep(self._tick)

    def percent(self):
        return self.remaining() / self._duration

    def count(self):
        return int(self.percent() * self._count )

    def __bool__(self):
        return self.remaining() > 0


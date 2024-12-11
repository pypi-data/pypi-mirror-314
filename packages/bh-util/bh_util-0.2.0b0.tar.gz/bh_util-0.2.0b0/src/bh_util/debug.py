#!/usr/bin/env python3
import sys

class Debug:
    def __init__(self, stat=False):
        if stat: self.turn_on()
        else: self.turn_off()
    def turn_on(self):  sys._bh_debug = True
    def turn_off(self): sys._bh_debug = False
    def __bool__(self): return sys._bh_debug
    def err(self, text, end='\n'):
        if self:
            sys.stderr.write(text + end)
            sys.stderr.flush()


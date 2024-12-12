#!/usr/bin/env python3
import sys

class DebugSingleton:
    state = False

    def note(self, text, end='\n'):
        if self:
            sys.stderr.write(text + end)
            sys.stderr.flush()

    def __init__(self, stat=None):
        if stat == True:
            self.__class__.state=True
        elif stat == False:
            self.__class__.state=False

    def __bool__(self):
        return self.__class__.state

    def __repr__(self):
        return f'<Debug:{bool(self)}>'

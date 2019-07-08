#!/usr/bin/python
import os

class Config:
    def __init__(self, cheatPath):
        self._cheatPath=cheatPath
        return None

    def validate(self):
        if os.path.exists(os.path.expanduser(self._cheatPath)):
            self._cheatPath=os.path.expanduser(self._cheatPath)
            return True
        return False

    def getPath(self):
        return self._cheatPath

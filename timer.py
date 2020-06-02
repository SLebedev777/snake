# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 19:16:11 2020

@author: Семен
"""

import threading


class RepeatedTimer:
    """
    Taken from:
    https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
    """
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
          self._timer = threading.Timer(self.interval, self._run)
          self._timer.start()
          self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


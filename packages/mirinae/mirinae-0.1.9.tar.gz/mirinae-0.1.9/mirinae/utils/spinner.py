#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

import sys
import time
import threading

"""How to use the Spinner class
    spinner = Spinner("Loading")
    spinner.start()

    # Simulate a long-running process
    time.sleep(5)

    spinner.stop()
"""

class Spinner:
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def _animate(self):
        spinner_chars = "|/-\\"
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{self.message}... {spinner_chars[idx]}")
            sys.stdout.flush()
            idx = (idx + 1) % len(spinner_chars)
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\rDone!            \n")
        sys.stdout.flush()


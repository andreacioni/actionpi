import logging

from threading import Thread

class ActionPiWhatchdog(object):

    def __init__(self):
        pass

    def watch(self):
        Thread(self._watchdog_loop).start()

    def _watchdog_loop(self):
       logging.info("Watchdog is starting")

    def stop(self):
        pass
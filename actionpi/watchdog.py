import logging

from threading import Thread
from .system import AbstractSystem
from .camera import AbstractCamera

MAX_DISK_USAGE_PERCENT = 80

class ActionPiWhatchdog(object):

    def __init__(self, system: AbstractSystem, camera: AbstractCamera):
        self._system = system

    def watch(self):
        Thread(self._watchdog_loop).start()

    def _watchdog_loop(self):
       logging.info("Watchdog is starting")
       if self._system.get_disk_usage() >= MAX_DISK_USAGE_PERCENT:
           logging.warn("Disk usage is above the maximum %s/%s", self._system.get_disk_usage(), MAX_DISK_USAGE_PERCENT)
           

    def stop(self):
        logging.info("Watchdog is stopping")
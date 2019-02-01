import logging
import schedule
import time

from threading import Thread, Event
from .system import AbstractSystem
from .camera import AbstractCamera

MAX_DISK_USAGE_PERCENT = 80

RUN_CONTINUOSLY_INTERVAL = 1

STOP_INTERVAL = 1

class ActionPiWhatchdog(object):

    def __init__(self, system: AbstractSystem, camera: AbstractCamera):
        self._system = system
        self._camera = camera
        self._is_watching = Event()
        

    def watch(self,interval=10):
        # Run the watchdog every 10 secs
        schedule.every(interval).seconds.do(self._watchdog_loop)

        self._stop_scheduler = Event()

        class ScheduleThread(Thread):
            @classmethod
            def run(cls):
                while not self._stop_scheduler.is_set():
                    self._is_watching.set()
                    schedule.run_pending()
                    time.sleep(RUN_CONTINUOSLY_INTERVAL)
                self._stop_scheduler.clear()

        ScheduleThread().start()


    def is_triggered(self) -> bool:
        triggered = False

        if self._system.get_disk_usage() >= MAX_DISK_USAGE_PERCENT:
            logging.warn("Disk usage is above the maximum %s/%s", self._system.get_disk_usage(), MAX_DISK_USAGE_PERCENT)
            triggered = True
        
        return triggered

    def _watchdog_loop(self):
        logging.info("Watchdog is performing the scheduled job...")

        if self.is_triggered():
            logging.warn("Detected a risky situation! Stopping recording and preventing HW demages")
            self._camera.stop_recording()

    
    def is_watching(self):
        return self._is_watching.is_set()

    def unwatch(self):
        logging.debug("Stopping watchdog...")
        
        self._stop_scheduler.set()
        while self._stop_scheduler.is_set():
            time.sleep(STOP_INTERVAL)
        
        self._is_watching.clear()
        logging.info("Watchdog stopped")
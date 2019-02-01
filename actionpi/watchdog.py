import logging
import schedule
import time

from threading import Thread, Event
from .system import AbstractSystem
from .camera import AbstractCamera
from .exception import AlreadyRunningException

# Threshold
MAX_DISK_USAGE_PERCENT = 80
MAX_CPU_TEMPERATURE_PERCENT = 55

# Sleep intervals
WATCHDOG_TRIGGERED_INTERVAL = 120
SLEEP_INTERVAL = 1
STOP_INTERVAL = 1

class ActionPiWhatchdog(object):

    def __init__(self, system: AbstractSystem, camera: AbstractCamera):
        self._system = system
        self._camera = camera
        self._is_watching = Event()
        self._is_triggered = Event()
        self._interval = 10

    def watch(self,interval=10):

        if self._is_watching.is_set():
            raise AlreadyRunningException('Watchdog is already running')

        self._interval = interval

        # Run the watchdog every <interval> secs
        schedule.every(interval).seconds.do(self._watchdog_loop)

        self._stop_scheduler = Event()

        class ScheduleThread(Thread):
            @classmethod
            def run(cls):
                while not self._stop_scheduler.is_set():
                    self._is_watching.set()
                    schedule.run_pending()
                    time.sleep(SLEEP_INTERVAL)
                self._stop_scheduler.clear()

        ScheduleThread().start()
    
    def _perform_system_status_check(self) -> bool:
        # Disk usage check
        if self._system.get_disk_usage() >= MAX_DISK_USAGE_PERCENT:
            logging.warn("Disk usage is above the maximum %s/%s", self._system.get_disk_usage(), MAX_DISK_USAGE_PERCENT)
            self._is_triggered.set()
        
        # Temperature check
        if self._system.get_cpu_temp() >= MAX_CPU_TEMPERATURE_PERCENT:
            logging.warn("CPU temperature is above the maximum %s/%s", self._system.get_disk_usage(), MAX_CPU_TEMPERATURE_PERCENT)
            self._is_triggered.set()

        return self._is_triggered.is_set()

    def is_triggered(self) -> bool:
        return self._is_triggered.is_set()

    def _watchdog_loop(self):
        logging.info("Watchdog is performing the scheduled job...")

        if not self._is_triggered.is_set():
            logging.debug("Watchdog is not triggered perform system status check")
            
            if self._perform_system_status_check():
                self._camera.stop_recording()
                schedule.clear()
                schedule.every(WATCHDOG_TRIGGERED_INTERVAL).seconds.do(self._watchdog_loop)
        else:
            logging.debug("Watchdog is triggered perform system status check")
            if not self._perform_system_status_check():
                self._camera.start_recording()
                schedule.clear()
                schedule.every(self._interval).seconds.do(self._watchdog_loop)

    
    def is_watching(self):
        return self._is_watching.is_set()

    def unwatch(self):
        logging.debug("Stopping watchdog...")
        
        self._stop_scheduler.set()
        while self._stop_scheduler.is_set():
            time.sleep(STOP_INTERVAL)
        
        self._is_watching.clear()
        self._is_triggered.clear()
        self._stop_scheduler.clear()
        
        schedule.clear()

        logging.info("Watchdog stopped")
import logging
import schedule
import time

from threading import Thread, Event, RLock
from .system import AbstractSystem
from .camera import AbstractCamera

# Threshold
MAX_DISK_USAGE_PERCENT = 90
MAX_CPU_TEMPERATURE_PERCENT = 55

# Sleep intervals
SLEEP_INTERVAL = 1
STOP_INTERVAL = 1

class ActionPiWhatchdog(object):

    def __init__(self, system: AbstractSystem, camera: AbstractCamera):
        self._system = system
        self._camera = camera
        self._is_watching = Event()
        self._is_triggered = Event()
        self._stop_scheduler = Event()
        self._lock = RLock()
        self._interval = 10
        self._watchdog_triggered_interval = 120

    def watch(self,interval=10):
        with self._lock:
            if self._is_watching.is_set():
                return

            self._interval = interval

            # Run the watchdog every <interval> secs
            schedule.every(interval).seconds.do(self._watchdog_loop)

            class ScheduleThread(Thread):
                @classmethod
                def run(cls):
                    while not self._stop_scheduler.is_set():
                        schedule.run_pending()
                        time.sleep(SLEEP_INTERVAL)
                    self._stop_scheduler.clear()

            self._is_watching.set()

            ScheduleThread().start()
    
    def _perform_system_status_check(self) -> bool:
        healty = True

        # Disk usage check
        full_disks = list(filter(lambda i: i['percent'] >= MAX_DISK_USAGE_PERCENT, self._system.get_disks_usage()))
        if len(full_disks) > 0:
            logging.warning("Disk/s usage of %s is above the allowed maximum %s", full_disks, MAX_DISK_USAGE_PERCENT)
            healty = False
        
        # Temperature check
        if self._system.get_cpu_temp() >= MAX_CPU_TEMPERATURE_PERCENT:
            logging.warning("CPU temperature is above the maximum %s/%s", self._system.get_cpu_temp(), MAX_CPU_TEMPERATURE_PERCENT)
            healty = False

        return healty

    def is_triggered(self) -> bool:
        with self._lock:
            return self._is_triggered.is_set()

    def _watchdog_loop(self):
        logging.info("Watchdog is performing the scheduled job...")

        if not self._is_triggered.is_set():
            logging.debug("Watchdog is not triggered perform system status check")
            
            if not self._perform_system_status_check():
                self._is_triggered.set()
                self._camera.stop_recording()
                schedule.clear()
                schedule.every(self._interval).seconds.do(self._watchdog_loop)
        else:
            logging.debug("Watchdog is triggered perform system status check")
            if self._perform_system_status_check():
                self._is_triggered.clear()
                self._camera.start_recording()
                schedule.clear()
                schedule.every(self._watchdog_triggered_interval).seconds.do(self._watchdog_loop)

    
    def is_watching(self):
        with self._lock:
            return self._is_watching.is_set()

    def set_watchdog_triggered_interval(self, interval: int):
        self._watchdog_triggered_interval = interval

    def get_camera(self) -> AbstractCamera:
        return self._camera

    def get_system(self) -> AbstractSystem:
        return self._system

    def unwatch(self):
        with self._lock:
            if self._is_watching.is_set():
                logging.debug("Stopping watchdog...")
                
                self._stop_scheduler.set()
                while self._stop_scheduler.is_set():
                    time.sleep(STOP_INTERVAL)
                
                self._is_watching.clear()
                self._is_triggered.clear()
                self._stop_scheduler.clear()
                
                schedule.clear()

                logging.info("Watchdog stopped")
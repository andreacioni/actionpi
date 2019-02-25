import logging

from .camera import AbstractCamera
from .system import AbstractSystem

class AbstractIO():
    def __init__(self, camera: AbstractCamera, systen: AbstractSystem, gpio_number: int):
        self._camera = camera
        self._system = systen
        self._gpio_number = gpio_number
    
    def start_monitoring(self):
        logging.info("Start monitoring GPIO {}".format(self._gpio_number))

    def close(self):
        logging.info("Stopping monitoring GPIO {}".format(self._gpio_number))
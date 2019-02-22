import logging

from .camera import AbstractCamera

class AbstractIO():
    def __init__(self, camera: AbstractCamera, gpio_number: int):
        self._camera = camera
        self._gpio_number = gpio_number
    
    def start_monitoring(self):
        logging.info("Start monitoring GPIO {}".format(self._gpio_number))

    def close(self):
        logging.info("Stopping monitoring GPIO {}".format(self._gpio_number))
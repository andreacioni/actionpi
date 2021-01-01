import logging

from flask.app import Config

from .camera import AbstractCamera
from .system import AbstractSystem

class AbstractIO():
    def __init__(self, camera: AbstractCamera, system: AbstractSystem, config: Config):
        self._camera = camera
        self._system = system
        self._config = config
    
    def start_monitoring(self):
        logging.info("Start monitoring GPIO {}".format(self._config['GPIO_SWITCH']))

    def close(self):
        logging.info("Stopping monitoring GPIO {}".format(self._config['GPIO_SWITCH']))
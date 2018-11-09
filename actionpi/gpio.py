import logging

from .camera import AbstractCamera
from abc import ABC, abstractmethod

class AbstractIO(ABC):
    def __init__(self, camera: AbstractCamera, gpio_number: int):
        self.camera = camera
    
    @abstractmethod
    def start_monitoring(self):
        pass

    @abstractmethod
    def close(self):
        pass
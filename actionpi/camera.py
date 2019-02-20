import logging

from abc import ABC, abstractmethod
from threading import RLock

class AbstractCamera(ABC):
    
    def __init__(self,width: int, heigth: int, fps: int, output_file: str):
        self._lock = RLock()
        with self._lock:
            self._width = width
            self._heigth = heigth
            self._fps = fps
            self._output_file = output_file

            self._camera = None

    def start_recording(self):
        logging.info('Recording %ix%i (%i FPS) video to %s', self._width, self._heigth, self._fps, self._output_file)
        with self._lock:
            self._start()
            

    def change_framerate(self, fps: int):
        logging.debug('Changing FPS to %i', fps)
        with self._lock:
            self.stop_recording()
            self._fps = fps
            self.start_recording()

    def stop_recording(self):
        logging.info('Stopping recording')
        with self._lock:
            self._stop()

    def is_recording(self) -> bool:
        with self._lock:
            return self._recording()

    def get_framerate(self) -> int:
        with self._lock:
            return self._fps

    @abstractmethod
    def capture_frame(self) -> str:
        pass

    @abstractmethod
    def set_led_status(self, status: bool):
        pass

    @abstractmethod
    def _start(self):
        pass

    @abstractmethod
    def _stop(self):
        pass

    @abstractmethod
    def _recording(self) -> bool:
        pass
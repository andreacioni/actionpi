import logging
try:
    import picamera
except ImportError:
    pass #TODO replace with mock import

from threading import RLock

class ActionPiCamera(object):

    def __init__(self,width: int, heigth: int, fps: int, output_file: str):
        self._lock = RLock()
        with self._lock:
            self._width = width
            self._heigth = heigth
            self._fps = fps
            self._output_file = open(output_file, 'wb')

            self._camera = None

    def start_recording(self):
        logging.debug('Recording %ix%i (%i FPS) video to %s', self._width, self._heigth, self._fps, self._output_file)
        with self._lock:
            self._camera = picamera.PiCamera(resolution= (self._width, self._heigth), framerate=self._fps)

            self._camera.start_recording(self._output_file)

    def change_framerate(self, fps):
        logging.debug('Changing FPS to %i', fps)
        with self._lock:
            self.stop_recording()
            self._fps = fps
            self.start_recording()


    def stop_recording(self):
        logging.debug('Stopping recording')
        with self._lock:
            self._camera.stop_recording()
            self._camera.close()
            self._camera = None

    def is_recording(self) -> bool:
        with self._lock:
            return (self._camera is not None) and (self._camera.recording)

    def get_framerate(self) -> int:
        with self._lock:
            if self._camera is not None:
                return self._camera.framerate
            else:
                return 0
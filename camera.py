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
            self._output_file = open(output_file, 'w')

            self._camera = None

    def start_recording(self, quality=0):
        with self._lock:
            print('Recording {}x{} ({} FPS) video to {}'.format(self._width, self._heigth, self._fps, self._output_file))
            
            self._camera = picamera.PiCamera(resolution= (self._width, self._heigth), framerate=self._fps)

            self._camera.start_recording(self._output_file,quality=quality)

    def set_quality(self, quality):
        with self._lock:
            self.stop_recording()
            self._camera.framerate()
            self._camera.start_recording(quality)


    def stop_recording(self):
        with self._lock:
            self._camera.stop_recording()
            self._camera.close()
            self._camera = None

    def is_recording(self) -> bool:
        with self._lock:
            return (self._camera is not None) and (self._camera.recording)

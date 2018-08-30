try:
    import picamera
except ImportError:
    pass #TODO replace with mock import

from threading import RLock

class ActionPiCamera(object):

    def __init__(self,width: int, heigth: int, fps: int, output_file: str):
        self._width = width
        self._heigth = heigth
        self._fps = fps
        self._output_file = output_file
        
        self._camera = None
        self._lock = RLock()


    def start_recording(self):
        with self._lock:
            print('Recording {}x{} ({} FPS) video to {}'.format(self._width, self._heigth, self._fps, self._output_file))

            if self._camera is None:
                self._camera = picamera.PiCamera()
            
            self._camera.resolution = (self._width, self._heigth)
            self._camera.framerate = self._fps


            self._camera.start_recording(self._output_file)

    def stop_recording(self):
        with self._lock:
            self._camera.stop_recording()

    def is_recording(self) -> bool:
        with self._lock:
            return self._camera.recording

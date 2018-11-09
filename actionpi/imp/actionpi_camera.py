from actionpi import AbstractCamera

try:
    from picamera import PiCamera
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module picamera installed")

class ActionPiCamera(AbstractCamera):

    def _start(self):
        self._camera = PiCamera(resolution= (self._width, self._heigth), framerate=self._fps)
        self._camera.start_recording(self._output_file)

    def stop_recording(self):
        self._camera.stop_recording()
        self._camera.close()
        self._camera = None

    def _recording(self) -> bool:
        return (self._camera is not None) and (self._camera.recording)

    def get_framerate(self) -> int:
        if self._camera is not None:
            return int(self._camera.framerate)
        else:
            return 0
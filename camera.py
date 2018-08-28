try:
    import picamera
except ImportError:
    pass #TODO replace with mock import

class ActionPiCamera(object):

    def __init__(self,width, heigth, fps, time, output_file):
        self._width = width
        self._heigth = heigth
        self._fps = fps
        self._time = time
        self._output_file = output_file

        self._camera = picamera.PiCamera()
        self._camera.resolution = (self._width, self._heigth)
        self._camera.framerate = self._fps

    def start_recording(self):
        print('Recording {}x{} ({} FPS) video for {}s to {}'.format(self._width, self._heigth, self._fps, self._time, self._output_file))

        self._camera.start_recording(self._output_file)

        if self._time != 0:
            self._camera.wait_recording(self._time)

    def stop_recording(self):
        self._camera.stop_recording()

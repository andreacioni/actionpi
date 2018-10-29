import logging
try:
    from gpiozero import Button
except ImportError:
    raise RuntimeError("not a Raspbian image")


class ActionPiIO(object):

    def __init__(self, camera, gpio):
        self.camera = camera
        self.button = Button(gpio)
    
    def start_monitoring(self):
        logging.info("Start monitoring GPIO {}".format(self.button.pin.number))
        self.button.when_pressed = self.camera.start_recording()
        self.button.when_released = self.camera.stop_recording()

        if self.button.is_pressed:
            self.camera.start_recording()

    def close(self):
        self.button.close()
        self.button = None
from actionpi import AbstractCamera

try:
    from gpiozero import Button
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module gpiozero installed")


class ActionPiIO(AbstractCamera):

    def __init__(self, camera: AbstractCamera, gpio_number):
        super(ActionPiIO, self).__init__(camera, gpio_number)
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
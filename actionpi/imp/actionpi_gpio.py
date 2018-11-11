import logging

from actionpi import AbstractIO, AbstractCamera

try:
    from gpiozero import Button
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module gpiozero installed")


class ActionPiIO(AbstractIO):

    def __init__(self, camera: AbstractCamera, gpio_number: int):
        super(ActionPiIO, self).__init__(camera, gpio_number)
        self.button = Button(gpio_number)
    
    def start_monitoring(self):
        super(ActionPiIO, self).start_monitoring()
        self.button.when_pressed = self._camera.start_recording()
        self.button.when_released = self._camera.stop_recording()

        if self.button.is_pressed:
            self._camera.start_recording()

    def close(self):
        super(ActionPiIO, self).close()
        self.button.close()
        self.button = None
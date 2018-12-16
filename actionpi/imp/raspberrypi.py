import logging
import subprocess
import psutil

from actionpi import AbstractIO, AbstractCamera, AbstractSystem

try:
    from gpiozero import Button
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module gpiozero installed")

try:
    from picamera import PiCamera
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module picamera installed")

class RaspberryPiCamera(AbstractCamera):

    def _start(self):
        self._camera = PiCamera(resolution= (self._width, self._heigth), framerate=self._fps)
        self._camera.start_recording(self._output_file)

    def _stop(self):
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

class RaspberryPiSystem(AbstractSystem):
    def get_cpu_temp(self) -> float:
        try:
            temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
            return temp
        except IOError:
            return 0

    def get_cpu_percent(self) -> int:
        return psutil.cpu_percent(interval=None)

    def get_disk_usage(self) -> int:
        return psutil.disk_usage('/').percent
    
    def get_ram_usage(self) -> int:
        return psutil.virtual_memory().percent

    def halt_system(self):
        subprocess.run(["shutdown", "-H", "now"])

    def enable_hotspot(self) -> bool:
        pass

    def disable_hotspot(self) -> bool:
        pass

class RaspberryPiIO(AbstractIO):

    def __init__(self, camera: AbstractCamera, gpio_number: int):
        super().__init__(camera, gpio_number)
        self.button = Button(gpio_number)
    
    def start_monitoring(self):
        super().start_monitoring()
        self.button.when_pressed = self._camera.start_recording()
        self.button.when_released = self._camera.stop_recording()

        if self.button.is_pressed:
            self._camera.start_recording()

    def close(self):
        super().close()
        self.button.close()
        self.button = None
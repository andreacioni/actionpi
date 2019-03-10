import logging
import subprocess
import psutil

from os import path
from pathlib import Path

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

    def __init__(self,width: int, heigth: int, fps: int, rotation: int, output_dir: str):
        super().__init__(width, heigth, fps, rotation, output_dir)
        self._first_run = True
        self._video_file = None

    def _start(self):
        if self._camera is None:
            self._camera = PiCamera(resolution= (self._width, self._heigth), framerate=self._fps)

            self._camera.rotation = self._rotation
            
            if self._first_run:
                self._video_file = open(self._output_file, 'wb')
                self._first_run = False
            else:
                self._video_file = open(self._output_file, 'ab')

            self._camera.start_recording(self._video_file)

    def _stop(self):
        if self._camera is not None:
            self._camera.stop_recording()
            self._camera.close()
            self._video_file.close()
            self._video_file = None
            self._camera = None

    def _recording(self) -> bool:
        return (self._camera is not None) and (self._camera.recording)

    def get_framerate(self) -> int:
        if self._camera is not None:
            return int(self._camera.framerate)
        else:
            return 0
    
    def set_led_status(self, status: bool):
        if self._camera is not None:
            self._camera.led = status

    def capture_frame(self) -> str:
        if self._camera is not None:
            self._camera.capture(path.join(self._output_dir, 'capture.jpg'), use_video_port=True)

class RaspberryPiSystem(AbstractSystem):
    def get_cpu_temp(self) -> float:
        try:
            temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
            return temp
        except IOError:
            return 0

    def get_cpu_percent(self) -> int:
        return psutil.cpu_percent(interval=None)

    def get_disks_usage(self) -> list:
        disk_usages = list()
        for part in psutil.disk_partitions(all=False):
            mountpoint = part.mountpoint
            usage = psutil.disk_usage(mountpoint)
            disk_usages.append({
                'mountpoint' : mountpoint,
                'percent' : usage.percent,
                'total' : usage.total,
                'used' : usage.used
            })
        return disk_usages
    
    def get_ram_usage(self) -> int:
        return psutil.virtual_memory().percent

    def halt_system(self):
        subprocess.run(["shutdown", "-H", "now"])

    def reboot_system(self):
        subprocess.run(["shutdown", "-r", "now"])

    def enable_hotspot(self) -> bool:
        Path('/boot/wifi_hotspot').touch()
        try:
            Path('/boot/wifi_client').unlink()
        except FileNotFoundError:
            pass
        return True

    def disable_hotspot(self) -> bool:
        Path('/boot/wifi_client').touch()
        try:
            Path('/boot/wifi_hotspot').unlink()
        except FileNotFoundError:
            pass
        return True

    def get_hw_revision(self) -> str:
        hw_rev = "00000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:8]=='Revision':
                    hw_rev = line[10:]
            f.close()
        except:
            hw_rev = "00000"

        return hw_rev

    def get_serial(self) -> str:
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"

        return cpuserial

    def mount_rw(self):
        Path('/boot/rw').touch()

class RaspberryPiIO(AbstractIO):

    def __init__(self, camera: AbstractCamera, system: AbstractSystem, gpio_number: int):
        super().__init__(camera, system, gpio_number)
        self.button = Button(gpio_number, bounce_time=1)
    
    def start_monitoring(self):
        super().start_monitoring()
        self.button.when_pressed = self._camera.start_recording
        self.button.when_released = self._system.halt_system
        
        if self.button.is_pressed:
            self._camera.start_recording()

    def close(self):
        super().close()
        self.button.close()
        self.button = None
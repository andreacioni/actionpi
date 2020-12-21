import logging
import subprocess
import psutil
import os
import re

from io import BytesIO
from pathlib import Path
from time import sleep

from actionpi import AbstractIO, AbstractCamera, AbstractSystem

try:
    from gpiozero import Button
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module gpiozero installed")

try:
    from picamera import PiCamera
except (ImportError, ModuleNotFoundError) as e:
    raise ImportError("No module picamera installed")

WPA_CONFIG_FILE_TEMPLATE="""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="%s"
    psk="%s"
    scan_ssid=1
}
"""

WPA_MIN_LENGTH_PASSWORD = 8

class RaspberryPiCamera(AbstractCamera):

    def __init__(self,width: int, heigth: int, fps: int, rotation: int, output_dir: str, rolling_size: int, rolling_nums: int):
        super().__init__(width, heigth, fps, rotation, output_dir, rolling_size, rolling_nums)


    def _start(self):
        if self._camera is None:
            self._camera = PiCamera(resolution= (self._width, self._heigth), framerate=self._fps)
            self._camera.rotation = self._rotation
            self._camera.start_recording(self._video_file, format='h264')

    def _stop(self):
        if self._camera is not None:
            self._camera.stop_recording()
            self._camera.close()
            self._camera = None

    def _recording(self) -> bool:
        return (self._camera is not None) and (self._camera.recording)

    def _support_split(self) -> bool:
        return True
    
    def _split_recording(self):
        self._camera.split_recording(self._video_file)

    def get_framerate(self) -> int:
        if self._camera is not None:
            return int(self._camera.framerate)
        else:
            return 0
    
    def set_led_status(self, status: bool):
        if self._camera is not None:
            self._camera.led = status

    def capture_frame(self) -> BytesIO:
        if self._camera is not None:
            capture_stream = BytesIO()
            self._camera.capture(capture_stream, 'jpeg', resize=(320, 240), use_video_port=True)
            capture_stream.seek(0)
            return capture_stream

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
    
    def get_wifi_mode(self) -> str:
        output = subprocess.run(["/sbin/iwconfig", "wlan0"], universal_newlines=True).stdout
        if output is not None and len(output) > 0:
            logging.debug('iwconfig output: {}'.format(output))
            match = re.search(r'Mode:([-\w]+)\s', output)
            if match:
                return match.group(1)
            else:
                logging.warn("No match!")
        else:
            logging.error('No output from subprocess')

        return None
        
    def enable_hotspot(self, password) -> bool:
        if password is not None \
            and isinstance(password, str)  \
            and len(password) >= WPA_MIN_LENGTH_PASSWORD:
            
            logging.info('Using new hotspot password: "{}"'.format(password))
            with open("/boot/wifi_hotspot", "w") as wifi_hotspot_file:
                print(password, file=wifi_hotspot_file)
        else:
            logging.info('Using old password')

        try:
            Path('/boot/wifi_client').unlink()
        except FileNotFoundError:
            logging.error('Failed to unlink')
            
        return True

    def connect_to_ap(self, ssid, password) -> bool:
        Path('/boot/wifi_client').touch()
        try:
            Path('/boot/wifi_hotspot').unlink()
        except FileNotFoundError:
            logging.error('Failed to unlink')

        if(ssid is not None and password is not None \
            and isinstance(ssid, str) and isinstance(password, str)
            and len(ssid) > 0 and len(password) >= WPA_MIN_LENGTH_PASSWORD):
            logging.debug('Using new AP parameter: SSID: "{}"; password: "{}"'.format(ssid, password))
            
            with open("/boot/wpa_supplicant.conf", "w") as wpa_supplicant_file:
                print(WPA_CONFIG_FILE_TEMPLATE.format(ssid, password), file=wpa_supplicant_file)
        else:
            logging.info('Using old WiFi configuration')

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

    def mount_ro(self):
        Path('/boot/rw').unlink()

    def will_mount_rw(self) -> bool:
        return Path('/boot/rw').exists() and Path('/boot/rw').is_file()

class RaspberryPiIO(AbstractIO):

    def __init__(self, camera: AbstractCamera, system: AbstractSystem, gpio_number: int):
        super().__init__(camera, system, gpio_number)
        self.button = Button(gpio_number, bounce_time=0.2)
    
    def start_monitoring(self):
        super().start_monitoring()
        self.button.when_pressed = self._start_recording_handler
        self.button.when_released = self._stop_recording_handler
        
        if self.button.is_pressed:
            self._camera.start_recording()

    def _start_recording_handler(self):
        self._camera.start_recording()

    def _stop_recording_handler(self):
        self._camera.stop_recording()
        sleep(1)
        self._system.halt_system()

    def close(self):
        super().close()
        self.button.close()
        self.button = None

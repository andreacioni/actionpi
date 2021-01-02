from io import BytesIO

from flask.app import Config

from actionpi import AbstractCamera, AbstractSystem, AbstractIO

class MockSystem(AbstractSystem):

    def __init__(self):
        self._cpu_temp = 20
        self._cpu_percent = 33
        self._mounted_rw = False
        self._disks_usage = [
            {'mountpoint':'/', 'percent' : 10, 'rw': False},
            {'mountpoint':'/media/recordings', 'percent' : 50, 'rw': self._mounted_rw}
        ]
        self._ram_usage = 60
        self._wifi_mode = 'Managed'

    def get_cpu_temp(self) -> float:
        return self._cpu_temp
    
    def set_cpu_temp(self, temp: float):
        self._cpu_temp = temp

    def get_cpu_percent(self) -> int:
        return self._cpu_percent
    
    def set_cpu_percent(self, percent: int):
        self._cpu_percent = percent

    def get_disks_usage(self) -> list:
        self._disks_usage[0]['rw'] = self._mounted_rw
        return self._disks_usage

    def set_disks_usage(self, usages: list):
        self._disks_usage = usages
    
    def get_ram_usage(self) -> int:
        return self._ram_usage

    def set_ram_usage(self, usage: int):
        self._ram_usage = usage

    def halt_system(self):
        pass

    def enable_hotspot(self, password) -> bool:
        self._wifi_mode = 'Master'
        return True

    def connect_to_ap(self, country_code, ssid, password) -> bool:
        self._wifi_mode = 'Managed'
        return True

    def get_wifi_mode(self) -> str:
        return self._wifi_mode

    def mount_rw(self):
        self._mounted_rw = True

    def mount_ro(self):
        self._mounted_rw = False

    def will_mount_rw(self) -> bool:
        return self._mounted_rw

    def reboot_system(self):
        pass

class MockCamera(AbstractCamera):

    def __init__(self, config: Config):
        super(MockCamera, self).__init__(config)
        self.__recording = False

    def _start(self):
        self.__recording = True

    def _stop(self):
        self.__recording = False

    def _recording(self) -> bool:
        return self.__recording

    def capture_frame(self):
        if self.__recording == True:
            buff = BytesIO(b'1234567890')
            buff.seek(0)
            return buff
    
    def set_led_status(self):
        pass

    def _split_recording(self):
        pass

    def _support_split(self) -> bool:
        return False

class MockIO(AbstractIO):

    def __init__(self, camera: AbstractCamera, system: AbstractSystem, config: Config):
        super().__init__(camera, system, config)
    
    def start_monitoring(self):
        super().start_monitoring()

    def close(self):
        super().close()

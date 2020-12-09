from io import BytesIO
from actionpi import AbstractCamera, AbstractSystem, AbstractIO

class MockSystem(AbstractSystem):

    def __init__(self):
        self._cpu_temp = 20
        self._cpu_percent = 33
        self._disks_usage = [{'mountpoint':'/', 'percent' : 10}]
        self._ram_usage = 60

    def get_cpu_temp(self) -> float:
        return self._cpu_temp
    
    def set_cpu_temp(self, temp: float):
        self._cpu_temp = temp

    def get_cpu_percent(self) -> int:
        return self._cpu_percent
    
    def set_cpu_percent(self, percent: int):
        self._cpu_percent = percent

    def get_disks_usage(self) -> list:
        return self._disks_usage

    def set_disks_usage(self, usages: list):
        self._disks_usage = usages
    
    def get_ram_usage(self) -> int:
        return self._ram_usage

    def set_ram_usage(self, usage: int):
        self._ram_usage = usage

    def halt_system(self):
        pass

    def enable_hotspot(self) -> bool:
        return True

    def disable_hotspot(self) -> bool:
        return True

class MockCamera(AbstractCamera):

    def __init__(self, rolling_size=0, rolling_num=0):
        super(MockCamera, self).__init__(1024, 768, 20, 0, ".", rolling_size, rolling_num)
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

    def __init__(self):
        super().__init__(None, None, 0)
    
    def start_monitoring(self):
        super().start_monitoring()

    def close(self):
        super().close()

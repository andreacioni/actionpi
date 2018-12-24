from actionpi import AbstractSystem

class MockSystem(AbstractSystem):

    def __init__(self):
        self._cpu_temp = 20
        self._cpu_percent = 33
        self._disk_usage = 10
        self._ram_usage = 60

    def get_cpu_temp(self) -> float:
        return self._cpu_temp
    
    def set_cpu_temp(self, temp: float):
        self._cpu_temp = temp

    def get_cpu_percent(self) -> int:
        return self._cpu_percent
    
    def set_cpu_percent(self, percent: int):
        self._cpu_percent = percent

    def get_disk_usage(self) -> int:
        return self._disk_usage

    def set_disk_usage(self, usage: int):
        self._disk_usage = usage
    
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
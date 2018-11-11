from actionpi import AbstractSystem

class MockSystem(AbstractSystem):
    def get_cpu_temp(self) -> float:
        return 20
    def get_cpu_percent(self) -> int:
        return 33

    def get_disk_usage(self) -> int:
        return 10
    
    def get_ram_usage(self) -> int:
        return 60

    def halt_system(self):
        pass

    def enable_hotspot(self) -> bool:
        return True

    def disable_hotspot(self) -> bool:
        return True
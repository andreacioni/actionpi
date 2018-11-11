import subprocess
import psutil

from actionpi import AbstractSystem

class ActionPiSystem(AbstractSystem):
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
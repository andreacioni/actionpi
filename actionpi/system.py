import subprocess
import psutil

class AbstractSystem(object):
    def get_cpu_temp(self) -> float:
        raise NotImplementedError('get_cpu_temp is not implemented')

    def get_cpu_percent(self) -> int:
        raise NotImplementedError('get_cpu_percent is not implemented')

    def get_disk_usage(self) -> int:
        raise NotImplementedError('get_disk_usage is not implemented')
    
    def get_ram_usage(self) -> int:
        raise NotImplementedError('get_ram_usage is not implemented')

    def halt_system(self):
        raise NotImplementedError('halt_system is not implemented')

    def enable_hotspot(self) -> bool:
        raise NotImplementedError('enable_hotspot is not implemented')

    def disable_hotspot(self) -> bool:
        raise NotImplementedError('disable_hotspot is not implemented')

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
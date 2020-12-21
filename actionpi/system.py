class AbstractSystem(object):
    def get_cpu_temp(self) -> float:
        raise NotImplementedError('get_cpu_temp is not implemented')

    def get_cpu_percent(self) -> int:
        raise NotImplementedError('get_cpu_percent is not implemented')

    def get_disks_usage(self) -> list:
        raise NotImplementedError('get_disks_usage is not implemented')
    
    def get_ram_usage(self) -> int:
        raise NotImplementedError('get_ram_usage is not implemented')

    def halt_system(self):
        raise NotImplementedError('halt_system is not implemented')

    def reboot_system(self):
        raise NotImplementedError('reboot_system is not implemented')

    def enable_hotspot(self, password) -> bool:
        raise NotImplementedError('enable_hotspot is not implemented')

    def connect_to_ap(self, ssid, password) -> bool:
        raise NotImplementedError('connect_to_ap is not implemented')

    def is_hotspot_enabled(self) -> bool:
        raise NotImplementedError('is_hotspot_enabled is not implemented')
    
    def get_hw_revision(self) -> str:
        raise NotImplementedError('get_hw_revision is not implemented')
    
    def get_serial(self) -> str:
        raise NotImplementedError('get_serial is not implemented')
    
    def mount_rw(self):
        raise NotImplementedError('mount_rw is not implemented')

    def mount_ro(self):
        raise NotImplementedError('mount_ro is not implemented')

    def will_mount_rw(self) -> bool:
        raise NotImplementedError('will_mount_rw is not implemented')


def get_cpu_temp() -> float:
    try:
        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
        return temp
    except IOError:
        return 0
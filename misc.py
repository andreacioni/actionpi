def get_cpu_temp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    print('Current CPU temperature is: {} C'.format(temp))
    return temp
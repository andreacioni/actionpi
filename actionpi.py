import io
import random
import argparse
import picamera

from version import name, vers

def get_cpu_temp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    print('Current CPU temperature is: {} C'.format(temp))
    return temp


#Parsing arguments
parser = argparse.ArgumentParser('{} - v.{}'.format(name, vers))
parser.add_argument('-w', '--width', \
                    metavar='width',
                    default=1920,
                    help='file containing the main setting of autobot')
parser.add_argument('-h', '--heigth',\
                    metavar='heigth',
                    default=1080,
                    help='file containing the configuration for autobot istance')
parser.add_argument('-f', '--fps',\
                    metavar='fps',
                    default=20,
                    help='file containing the configuration for autobot istance')
parser.add_argument('-b', '--bps',\
                    metavar='bps',
                    default=1200000,
                    help='file containing the configuration for autobot istance')
parser.add_argument('-t', '--time',\
                    metavar='rec_sec',
                    default=10,
                    help='file containing the configuration for autobot istance')
parser.add_argument('-l', '--log_level', \
                    metavar='log_level', \
                    default='WARN', \
                    choices=['DEBUG', 'INFO', 'WARN', 'ERROR'], \
                    help='file containing the configuration for autobot istance')

args = parser.parse_args()

camera = picamera.PiCamera()
camera.resolution = (args.width, args.heigth)
camera.start_recording('video.h264')
camera.wait_recording(args.rec_sec)
camera.stop_recording()
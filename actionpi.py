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
parser.add_argument('-x', '--width', \
                    type=int,
                    default=1920,
                    help='width')
parser.add_argument('-y', '--heigth',\
                    type=int,
                    default=1080,
                    help='heigth')
parser.add_argument('-f', '--fps',\
                    type=int,
                    default=20,
                    help='fps')
parser.add_argument('-b', '--bps',\
                    type=int,
                    default=1200000,
                    help='framerate')
parser.add_argument('-t', '--time',\
                    type=int,
                    default=10,
                    help='rec_sec')
parser.add_argument('-l', '--log_level', \
                    metavar='log_level', \
                    default='WARN', \
                    choices=['DEBUG', 'INFO', 'WARN', 'ERROR'], \
                    help='file containing the configuration for autobot istance')

args = parser.parse_args()

print('Recording {}x{} ({} FPS) video'.format(args.width, args.heigth, args.fps))

camera = picamera.PiCamera()
camera.resolution = (args.width, args.heigth)
camera.framerate = args.fps
camera.start_recording('video.h264')
camera.wait_recording(args.time)
camera.stop_recording()
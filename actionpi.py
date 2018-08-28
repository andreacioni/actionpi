import io
import random
import argparse

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

from camera import ActionPiCamera
from api import ActionPiAPI
from version import name, vers

#Parsing arguments
parser = argparse.ArgumentParser('{} - v.{}'.format(name, vers))
parser.add_argument('host',
                    help='host')
parser.add_argument('port',
                    type=int,
                    help='host')
parser.add_argument('-x', '--width',
                    type=int,
                    default=1920,
                    help='width')
parser.add_argument('-y', '--heigth',
                    type=int,
                    default=1080,
                    help='heigth')
parser.add_argument('-f', '--fps',
                    type=int,
                    default=20,
                    help='fps')
parser.add_argument('-b', '--bps',
                    type=int,
                    default=1200000,
                    help='framerate')
parser.add_argument('-t', '--time',
                    type=int,
                    default=10,
                    help='rec_sec')
parser.add_argument('-o', '--output_file',
                    default='video.h264',
                    help='video.h264')
parser.add_argument('-l', '--log_level',
                    metavar='log_level',
                    default='WARN',
                    choices=['DEBUG', 'INFO', 'WARN', 'ERROR'],
                    help='file containing the configuration for autobot istance')

args = parser.parse_args()

camera = ActionPiCamera(args.width, args.heigth, args.fps, args.time, args.output_file)
api = ActionPiAPI(camera, args.host, args.port, True)

api.serve()
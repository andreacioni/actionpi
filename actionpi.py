import io
import random
import argparse

from camera import ActionPiCamera
from api import ActionPiAPI
from app import name, version
from gpio import ActionPiIO
from watchdog import ActionPiWhatchdog

#Parsing arguments
parser = argparse.ArgumentParser('{} - v.{}'.format(name, version))
parser.add_argument('host',
                    help='host')
parser.add_argument('port',
                    type=int,
                    help='host')
parser.add_argument('gpio',
                    type=int,
                    help='gpio')
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
                    help='bitrate')
parser.add_argument('-o', '--output_file',
                    default='video.h264',
                    help='video.h264')
parser.add_argument('-l', '--log_level',
                    metavar='log_level',
                    default='WARN',
                    choices=['DEBUG', 'INFO', 'WARN', 'ERROR'],
                    help='file containing the configuration for autobot istance')

args = parser.parse_args()

camera = ActionPiCamera(args.width, args.heigth, args.fps, args.output_file)
io = ActionPiIO(camera, args.gpio)
api = ActionPiAPI(camera, args.host, args.port, True)
watchdog = ActionPiWhatchdog()

watchdog.watch()
io.start_monitoring()
api.serve()

#Stopping all services

api.close()
io.close()
watchdog.stop()
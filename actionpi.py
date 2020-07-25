import io
import os
import random
import argparse
import logging

from logging.handlers import RotatingFileHandler
from pycommon import path

from actionpi import (
    ActionPiFactory,
    ActionPiAPI, 
    ActionPiWhatchdog, 
    AbstractCamera, 
    AbstractIO, 
    AbstractSystem,
    name, version
)

LOG_MAX_SIZE = 10000000
LOG_BACKUP_COUNT = 3

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
parser.add_argument('-r', '--rotation',
                    type=int,
                    default=0,
                    help='rotation')
parser.add_argument('-f', '--fps',
                    type=int,
                    default=20,
                    help='fps')
parser.add_argument('-b', '--bps',
                    type=int,
                    default=1200000,
                    help='bitrate')
parser.add_argument('-o', '--output_dir',
                    default='video.h264',
                    help='video.h264')
parser.add_argument('-p', '--platform',
                    default='raspberrypi',
                    help='platform')
parser.add_argument('--log_file',
                    default=None,
                    help='if defined, indicates the file used by the application to log')
parser.add_argument('-l', '--log_level',
                    metavar='log_level',
                    default='WARN',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                    help='file containing the configuration for autobot istance')

args = parser.parse_args()

# Sutup logger
if args.log_file is None:
    logging.basicConfig(
        level=logging.getLevelName(args.log_level)
    )
else:
    logging.basicConfig(
        handlers=[RotatingFileHandler(args.log_file, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT)], 
        level=logging.getLevelName(args.log_level)
    )

# Instatiate all dependencies
camera = ActionPiFactory.get_camera(args.platform, args.width, args.heigth, args.fps, args.rotation, args.output_dir, 5000000, 10)
system = ActionPiFactory.get_system(args.platform)
io = ActionPiFactory.get_io(args.platform, camera, system, args.gpio)
api = ActionPiAPI(camera, system, args.host, args.port, False)
watchdog = ActionPiWhatchdog(system, camera)

# Infer mountpoint of camera output directory
mount_point=path.find_mount_point(camera.get_output_dir())
logging.debug('Mountpoint of output directory %s is: %s', camera.get_output_dir(), mount_point)

# Run background tasks
watchdog.watch(disks_to_watch=[mount_point])
io.start_monitoring()

logging.info('Starting REST server...')
# Let's go!
api.serve()

# Stopping all services
api.close()
io.close()
watchdog.unwatch()

# Ensuring all data are written on disk

import io
import os
import random
import argparse
import logging

from flask import Flask

from logging.handlers import RotatingFileHandler
from pycommon import path

from actionpi import (
    ActionPiFactory,
    ActionPiAPI, 
    ActionPiWatchdog, 
    AbstractCamera, 
    AbstractIO, 
    AbstractSystem,
    name, version
)

#Parsing arguments
parser = argparse.ArgumentParser('{} - v.{}'.format(name, version))
parser.add_argument('-c', '--config_file',
                    help='Configuration file path')
args = parser.parse_args()

# Setup app
app = Flask(__name__, static_url_path='/')
app.config.from_pyfile(args.config_file)

# Sutup logger
if app.config['LOG_FILE'] is None:
    logging.basicConfig(
        level=logging.getLevelName(app.config['LOG_LEVEL'])
    )
else:
    logging.basicConfig(
        handlers=[RotatingFileHandler(app.config['LOG_FILE'], maxBytes=app.config['LOG_MAX_SIZE'], backupCount=app.config['LOG_BACKUP_COUNT'])], 
        level=logging.getLevelName(app.config['LOG_LEVEL'])
    )

# Instantiate all dependencies
camera = ActionPiFactory.get_camera(app.config)
system = ActionPiFactory.get_system(app.config)
io = ActionPiFactory.get_io(app.config, camera, system)
api = ActionPiAPI(app, camera, system)
watchdog = ActionPiWatchdog(system, camera, app.config)

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

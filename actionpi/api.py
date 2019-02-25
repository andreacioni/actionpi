import logging
import os

from .app import name, version
from .camera import AbstractCamera
from .system import AbstractSystem
from flask import Flask, render_template
from flask_restful import Api, Resource, abort, request

from flask.testing import FlaskClient


API_PREFIX = '/api'

class ActionPiAPI(object): 

    def __init__(self, camera: AbstractCamera, system: AbstractSystem, host: str, port: int, debug=False):
        self._host = host
        self._port = port
        self._debug = debug

        self._app = Flask(__name__)
        self._api = Api(self._app)

        #Setup routes
        self._api.add_resource(Start, API_PREFIX + '/start', resource_class_args=(camera,))
        self._api.add_resource(Stop, API_PREFIX + '/stop', resource_class_args=(camera,))
        self._api.add_resource(Status, API_PREFIX + '/status', resource_class_args=(camera, system))
        self._api.add_resource(Set, API_PREFIX + '/set', resource_class_args=(camera,))
        self._api.add_resource(Hotspot, API_PREFIX + '/hotspot', resource_class_args=(system, ))
        self._api.add_resource(Halt, API_PREFIX + '/halt', resource_class_args=(system,))
        self._api.add_resource(Reboot, API_PREFIX + '/reboot', resource_class_args=(system,))
        self._api.add_resource(Mount, API_PREFIX + '/mountrw', resource_class_args=(system,))

        #Static route
        self._app.add_url_rule('/', '_index', self._index)
    
    def _index(self):
        return render_template('index.html', app={"name":name, "version":version})

    def get_test_client(self) -> FlaskClient:
        """
            Only for test purpose
        """
        return self._app.test_client()

    def get_context(self):
        """
            Only for test purpose
        """
        return self._app.app_context()

    def serve(self):
        logging.info("Serving API (debug: %s)", self._debug)
        self._app.run(host=self._host, port=self._port, debug=self._debug)

    def close(self):
        pass

class Start(Resource):
    def __init__(self, camera: AbstractCamera):
        self._camera = camera

    def get(self):
        self._camera.start_recording()
        return '', 204

class Stop(Resource):
    def __init__(self, camera: AbstractCamera):
        self._camera = camera
    
    def get(self):
        self._camera.stop_recording()
        return '', 204

#TODO add more logic if needed in future
class Set(Resource):
    def __init__(self, camera: AbstractCamera):
        self._camera = camera
    
    def get(self, val: int):
        self._camera.change_framerate(val)

class Status(Resource):
    def __init__(self, camera: AbstractCamera, system: AbstractSystem):
        self._camera = camera
        self._system = system
    
    def get(self):
        return {
            'system': {
                'cpu_temperature': self._system.get_cpu_temp(),
                'cpu_load': self._system.get_cpu_percent(),
                'mem_usage': self._system.get_ram_usage(),
                'disk_usage': self._system.get_disks_usage()
            }, 
            'recording': self._camera.is_recording(),
            'framerate': self._camera.get_framerate()
        }

class Halt(Resource):
    def __init__(self, system: AbstractSystem):
        self._system = system

    def get(self):
        logging.info('Shutdown now')
        self._system.halt_system()

class Reboot(Resource):
    def __init__(self, system: AbstractSystem):
        self._system = system

    def get(self):
        logging.info('Reboot now')
        self._system.reboot_system()            

class Hotspot(Resource):
    def __init__(self, system: AbstractSystem):
        self._system = system

    def get(self):
        enable = request.args.get('enable')

        if enable == 'on':
            logging.info('enabling hotspot')
            if not self._system.enable_hotspot():
                abort(500)
        elif enable == 'off':
            logging.info('disabling hotspot')
            if not self._system.disable_hotspot():
                abort(500)
        else:
            logging.error('enable must be "on" or "off", received: %s', enable)
            return 'enable must be "on" or "off"', 400

        return '', 204

class Mount(Resource):
    def __init__(self, system: AbstractSystem):
        self._system = system

    def get(self):
        logging.info('enabling rw file system')
        self._system.mount_rw()
        return '', 204
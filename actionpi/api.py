import logging
import os

from .app import name, version
from .camera import AbstractCamera
from .system import AbstractSystem
from flask import Flask, render_template, send_file, Response
from flask_restful import Api, Resource, abort, request
from flask_cors import CORS

from flask.testing import FlaskClient


API_PREFIX = '/api'

class ActionPiAPI(object): 

    def __init__(self, app: Flask, camera: AbstractCamera, system: AbstractSystem):

        self._app = app
        self._api = Api(self._app)

        self._camera = camera
        self._system = system

        #CORS
        CORS(self._app)

        #Setup routes
        self._api.add_resource(Start, API_PREFIX + '/start', resource_class_args=(camera,))
        self._api.add_resource(Stop, API_PREFIX + '/stop', resource_class_args=(camera,))
        self._api.add_resource(Status, API_PREFIX + '/status', resource_class_args=(camera, system))
        self._api.add_resource(Set, API_PREFIX + '/set', resource_class_args=(camera,))
        self._api.add_resource(Hotspot, API_PREFIX + '/hotspot', resource_class_args=(system, ))
        self._api.add_resource(Halt, API_PREFIX + '/halt', resource_class_args=(system,))
        self._api.add_resource(Reboot, API_PREFIX + '/reboot', resource_class_args=(system,))
        self._api.add_resource(Mount, API_PREFIX + '/mount', resource_class_args=(system,))
        self._api.add_resource(Recordings, API_PREFIX + '/recordings', resource_class_args=(camera,))
        self._api.add_resource(Recording, API_PREFIX + '/recording/<string:filename>', resource_class_args=(camera,))

        #Static route
        self._app.add_url_rule('/', '_index', self._index)

        #Preview
        self._app.add_url_rule('/preview', '_preview', self._preview)

    def _index(self):
        return self._app.send_static_file('index.html')    

    def _preview(self):
        frame_buff = self._camera.capture_frame()
        if frame_buff is not None:
            return Response((b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_buff.read() + b'\r\n'),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return Response('', 409)

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
        logging.info("Serving API (debug: %s)", self._app.config['DEBUG'])
        self._app.run(host=self._app.config['HOST'], port=self._app.config['PORT'], debug=self._app.config['DEBUG'])

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
                'disk_usage': self._system.get_disks_usage(),
                'ap_mode': self._system.get_wifi_mode(),
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
        ssid = request.args.get('ssid')
        password = request.args.get('password')
        country_code = request.args.get('country_code')

        if enable == 'on':
            logging.info('enabling hotspot')
            if not self._system.enable_hotspot(password):
                abort(500)
        elif enable == 'off':
            logging.info('disabling hotspot and enable client mode (AP name: %s, password: %s)', ssid, password)
            if not self._system.connect_to_ap(country_code, ssid, password):
                abort(500)
        else:
            logging.error('enable must be "on" or "off", received: %s', enable)
            return 'enable must be "on" or "off"', 400

        return '', 204

class Mount(Resource):
    def __init__(self, system: AbstractSystem):
        self._system = system

    def get(self):
        mode = request.args.get('mode')
        
        if mode == 'rw':
            logging.info('enabling rw file system')
            self._system.mount_rw()
        elif mode == 'ro':
            logging.info('enabling ro file system')
            self._system.mount_ro()
        else:
            logging.error('mode must be "rw" or "ro", received: %s', mode)
            return 'mode must be "rw" or "ro"', 400

        return '', 204

class Recordings(Resource):
    def __init__(self, camera: AbstractCamera):
        self._camera = camera

    def get(self):
        logging.debug('listing files in %s', self._camera.get_output_dir())
        file_names = os.listdir(self._camera.get_output_dir())
        file_names = filter(lambda f: (f is not None) and f.endswith('.h264'), file_names)

        def to_obj(file_name) -> dict:
            return {
                'name': file_name,
                'size': os.path.getsize(os.path.join(self._camera.get_output_dir(), file_name))
            }
        
        return list(map(to_obj, file_names))

class Recording(Resource):
    def __init__(self, camera: AbstractCamera):
        self._camera = camera

    def get(self, filename: str):
        relative_path = os.path.join(self._camera.get_output_dir(), filename)
        absolute_path = os.path.abspath(relative_path)
        logging.debug('downloading file %s', absolute_path)
        if os.path.exists(absolute_path):
            return send_file(absolute_path)
        else:
            return {'message': 'no file in path {} exists'.format(absolute_path)}, 404
        

    
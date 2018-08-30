import os
import app
import psutil

from camera import ActionPiCamera
from misc import get_cpu_temp
from apistar import App, Route

class ActionPiAPI(object):

    def __init__(self, camera: ActionPiCamera, host: str, port: int, debug=False):
        self._camera = camera
        self._host = host
        self._port = port
        self._debug = debug

        #Declaring routes
        _routes = [
            Route('/api/start', method='GET', handler=self._start_recording),
            Route('/api/stop', method='GET', handler=self._stop_recording),
            Route('/api/status', method='GET', handler=self._get_status),
            Route('/api/quality', method='GET', handler=self._set_quality),
            Route('/control', method='GET', handler=self._control)
        ]

        #Serving static files
        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, 'static')
        templates_dir = os.path.join(base_dir, 'templates')

        self._api = App(routes=_routes, static_dir=static_dir, template_dir=templates_dir)


    def _start_recording(self):
        self._camera.start_recording()
    
    def _stop_recording(self):
        self._camera.stop_recording()

    def _set_quality(self, quality: int):
        print(quality)
        self._camera.set_quality(quality)

    def _get_status(self) -> dict:
        return {
            'system': {
                'cpu_temperature': get_cpu_temp(),
                'cpu_load':psutil.cpu_percent(interval=None),
            }, 'recording': self._camera.is_recording()
        }

    def _control(self):
        return self._api.render_template('index.html', app=app)

    def serve(self):
        self._api.serve(self._host, self._port, self._debug)



    

    
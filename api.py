import os

from misc import get_cpu_temp
from apistar import App, Route

class ActionCameraAPI(object):

    def __init__(self, host: str, port: int, debug=False):
        self._host = host
        self._port = port
        self._debug = debug

        #Declaring routes
        _routes = [
            Route('/api/start', method='GET', handler=self._start_recording),
            Route('/api/start', method='GET', handler=self._stop_recording),
            Route('/api/cputemp', method='GET', handler=self._get_cpu_temperature),
        ]

        #Serving static files
        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, 'static')

        self._api = App(routes=_routes, static_dir=static_dir, static_url='/')


    def _start_recording(self):
        pass
    
    def _stop_recording(self):
        pass

    def _get_cpu_temperature(self):
        return {'temperature': get_cpu_temp()}

    def serve(self):
        self._api.serve(self._host, self._port, self._debug)



    

    
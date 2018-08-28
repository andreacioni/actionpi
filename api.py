import os

from apistar import App, Route

class ActionCameraAPI(object):

    def __init__(self, host, port, debug=False):
        self._host = host
        self._port = port
        self._debug = debug

        _routes = [
            Route('/control', method='GET', handler=welcome),
        ]

        #Serving static files
        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, 'static')

        self._api = App(routes=_routes, static_dir=static_dir, static_url='/')

    def serve(self):
        app.serve(self._host, self._port, self._debug)



    

    
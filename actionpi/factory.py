from flask.app import Config

from . import AbstractCamera, AbstractIO, AbstractSystem

class ActionPiFactory(object):

    @staticmethod   
    def get_system(config: Config) -> AbstractSystem:
        if config['PLATFORM'] == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiSystem
            return RaspberryPiSystem()
        if config['PLATFORM'] == 'mock':
            from .imp.mock import MockSystem
            return MockSystem()
        else:
            raise RuntimeError('board system not supported: ' + config['PLATFORM'])

    @staticmethod
    def get_io(config: Config, camera: AbstractCamera, system: AbstractSystem) -> AbstractIO:
        if config['PLATFORM'] == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiIO
            return RaspberryPiIO(camera, system, config)
        if config['PLATFORM'] == 'mock':
            from .imp.mock import MockIO
            return MockIO(camera, system, config)
        else:
            raise RuntimeError('board system not supported: ' + config['PLATFORM'])

    @staticmethod
    def get_camera(config: Config) -> AbstractCamera:
        if config['PLATFORM'] == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiCamera
            return RaspberryPiCamera(config)
        if config['PLATFORM'] == 'mock':
            from .imp.mock import MockCamera
            return MockCamera(config)
        else:
            raise RuntimeError('board system not supported: ' + config['PLATFORM'])

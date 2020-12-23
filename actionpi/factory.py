from . import AbstractCamera, AbstractIO, AbstractSystem

class ActionPiFactory(object):

    @staticmethod   
    def get_system(board: str) -> AbstractSystem:
        if board == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiSystem
            return RaspberryPiSystem()
        if board == 'mock':
            from .imp.mock import MockSystem
            return MockSystem()
        else:
            raise RuntimeError('board system not supported:' + board)

    @staticmethod
    def get_io(board: str, camera: AbstractCamera, system: AbstractSystem, gpio: int) -> AbstractIO:
        if board == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiIO
            return RaspberryPiIO(camera, system, gpio)
        if board == 'mock':
            from .imp.mock import MockIO
            return MockIO()
        else:
            raise RuntimeError('board system not supported:' + board)

    @staticmethod
    def get_camera(board: str, width: int, heigth:int, fps:int, rotation: int, output_dir: str, rolling_size=0, rolling_nums=0) -> AbstractCamera:
        if board == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiCamera
            return RaspberryPiCamera(width, heigth, fps, rotation, output_dir, rolling_size, rolling_nums)
        if board == 'mock':
            from .imp.mock import MockCamera
            return MockCamera()
        else:
            raise RuntimeError('board system not supported:' + board)

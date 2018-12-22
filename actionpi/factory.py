from . import AbstractCamera, AbstractIO, AbstractSystem

class ActionPiFactory(object):

    @staticmethod   
    def get_system(board: str) -> AbstractSystem:
        if board == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiSystem
            return RaspberryPiSystem()
        else:
            raise RuntimeError('board system not supported:' + board)

    @staticmethod
    def get_io(board: str, camera: AbstractCamera, gpio: int) -> AbstractIO:
        if board == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiIO
            return RaspberryPiIO(camera, gpio)
        else:
            raise RuntimeError('board system not supported:' + board)

    @staticmethod
    def get_camera(board: str, width: int, heigth:int, fps:int, output_file: str) -> AbstractCamera:
        if board == 'raspberrypi':
            from .imp.raspberrypi import RaspberryPiCamera
            return RaspberryPiCamera(width, heigth, fps, output_file)
        else:
            raise RuntimeError('board system not supported:' + board)
from . import AbstractCamera, AbstractIO, AbstractSystem
from .imp.raspberrypi import RaspberryPiCamera, RaspberryPiIO, RaspberryPiSystem

def get_system(board: str) -> AbstractSystem:
    if board == 'raspberrypi':
        return RaspberryPiSystem()
    else:
        raise RuntimeError('board system not supported:' + board)

def get_io(board: str, camera: AbstractCamera, gpio: int) -> AbstractIO:
    if board == 'raspberrypi':
        return RaspberryPiIO(camera, gpio)
    else:
        raise RuntimeError('board system not supported:' + board)

def get_camera(board: str, width: int, heigth:int, fps:int, output_file: str) -> AbstractCamera:
    if board == 'raspberrypi':
        return RaspberryPiCamera(width, heigth, fps, output_file)
    else:
        raise RuntimeError('board system not supported:' + board)
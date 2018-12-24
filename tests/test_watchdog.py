import pytest
import time

from actionpi import ActionPiWhatchdog
from mocks.mock_camera import MockCamera
from mocks.mock_system import MockSystem

mock_sys = MockSystem()
mock_cam = MockCamera()

@pytest.fixture
def watchdog():
    return ActionPiWhatchdog(mock_cam, mock_sys)

def test_start_stop(watchdog: ActionPiWhatchdog):
    watchdog.watch()
    time.sleep(2)
    assert watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()

def test_camera_stop(watchdog: ActionPiWhatchdog):
    mock_cam.start_recording()
    assert mock_cam.is_recording()
    
    watchdog.watch(1)
    time.sleep(2)
    assert watchdog.is_watching()
    
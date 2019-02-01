import pytest
import time

from actionpi import ActionPiWhatchdog
from actionpi.exception import AlreadyRunningException

from mocks.mock_camera import MockCamera
from mocks.mock_system import MockSystem

mock_sys = MockSystem()
mock_cam = MockCamera()

@pytest.fixture
def watchdog():
    return ActionPiWhatchdog(mock_sys, mock_cam)

def test_start_stop(watchdog: ActionPiWhatchdog):
    watchdog.watch()
    time.sleep(2)
    assert watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    
def test_disk_percent_over_limit(watchdog: ActionPiWhatchdog):
    mock_cam.start_recording()
    assert mock_cam.is_recording()
    
    watchdog.watch(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    mock_sys.set_disk_usage(90)
    time.sleep(2)
    
    assert watchdog.is_triggered()
    assert not mock_cam.is_recording()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()


def test_cpu_temperature_over_limit(watchdog: ActionPiWhatchdog):
    mock_cam.start_recording()
    assert mock_cam.is_recording()
    
    watchdog.watch(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    mock_sys.set_cpu_temp(70)
    time.sleep(2)
    
    assert watchdog.is_triggered()
    assert not mock_cam.is_recording()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()

def test_already_running_exception(watchdog: ActionPiWhatchdog):
    mock_cam.start_recording()
    assert mock_cam.is_recording()
    
    watchdog.watch(1)
    time.sleep(2)

    assert watchdog.is_watching()
    with pytest.raises(AlreadyRunningException):
        watchdog.watch(1)

    watchdog.unwatch()
    time.sleep(2)

    assert not watchdog.is_watching()


import pytest
import time

from actionpi import ActionPiWhatchdog

from mocks.mock_camera import MockCamera
from mocks.mock_system import MockSystem

@pytest.fixture
def watchdog():
    wd = ActionPiWhatchdog(MockSystem(), MockCamera())
    return wd
    #yield wd
    #wd.unwatch()

def test_start_stop(watchdog: ActionPiWhatchdog):
    watchdog.watch()
    assert watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    
def test_disk_percent_over_limit(watchdog: ActionPiWhatchdog):
    watchdog.get_camera().start_recording()
    assert  watchdog.get_camera().is_recording()
    
    watchdog.watch(1)
    watchdog.set_watchdog_triggered_interval(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    watchdog.get_system().set_disks_usage({"/" : 90})
    time.sleep(2)
    
    assert watchdog.is_triggered()
    assert not  watchdog.get_camera().is_recording()

    watchdog.get_system().set_disks_usage({"/" : 20})
    time.sleep(2)
    
    assert not watchdog.is_triggered()
    assert watchdog.get_camera().is_recording()
    
    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    assert not watchdog.is_triggered()


def test_one_disk_of_two_percent_over_limit(watchdog: ActionPiWhatchdog):
    watchdog.get_camera().start_recording()
    assert  watchdog.get_camera().is_recording()
    
    watchdog.watch(1)
    watchdog.set_watchdog_triggered_interval(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    watchdog.get_system().set_disks_usage({"/a" : 10, "/b" : 90})
    time.sleep(2)
    
    assert watchdog.is_triggered()
    assert not  watchdog.get_camera().is_recording()

    watchdog.get_system().set_disks_usage({"/a" : 10, "/b" : 20})
    time.sleep(2)
    
    assert not watchdog.is_triggered()
    assert watchdog.get_camera().is_recording()
    
    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    assert not watchdog.is_triggered()

def test_cpu_temperature_over_limit(watchdog: ActionPiWhatchdog):
    watchdog.get_camera().start_recording()
    assert watchdog.get_camera().is_recording()
    
    watchdog.watch(1)
    watchdog.set_watchdog_triggered_interval(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    watchdog.get_system().set_cpu_temp(70)
    time.sleep(2)

    assert watchdog.is_triggered()
    assert not watchdog.get_camera().is_recording()

    watchdog.get_system().set_cpu_temp(20)
    time.sleep(2)
    
    assert not watchdog.is_triggered()
    assert watchdog.get_camera().is_recording()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    assert not watchdog.is_triggered()

def test_multiple_unwatch(watchdog: ActionPiWhatchdog):

    assert not watchdog.is_watching()
    
    watchdog.unwatch()
    watchdog.unwatch()
    watchdog.unwatch()
    watchdog.unwatch()

    assert not watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
def test_multiple_watch(watchdog: ActionPiWhatchdog):
    watchdog.watch(1)
    watchdog.watch(1)
    watchdog.watch(1)
    watchdog.watch(1)

    assert watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()

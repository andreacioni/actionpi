import pytest
import time

from actionpi import ActionPiWatchdog

from actionpi.imp.mock import MockCamera
from actionpi.imp.mock import MockSystem

@pytest.fixture
def watchdog():
    wd = ActionPiWatchdog(MockSystem(), MockCamera())
    return wd
    #yield wd
    #wd.unwatch()

def test_start_stop(watchdog: ActionPiWatchdog):
    watchdog.watch()
    assert watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    
def test_disk_percent_over_limit(watchdog: ActionPiWatchdog):
    watchdog.get_camera().start_recording()
    assert  watchdog.get_camera().is_recording()
    
    watchdog.watch(1)
    watchdog.set_watchdog_triggered_interval(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    watchdog.get_system().set_disks_usage([{'mountpoint':'/', 'percent' : 90}])
    time.sleep(2)
    
    assert watchdog.is_triggered()
    assert not  watchdog.get_camera().is_recording()

    watchdog.get_system().set_disks_usage([{'mountpoint':'/', 'percent' : 20}])
    time.sleep(2)
    
    assert not watchdog.is_triggered()
    assert watchdog.get_camera().is_recording()
    
    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    assert not watchdog.is_triggered()

def test_disk_over_limit_not_watched(watchdog: ActionPiWatchdog):
    watchdog.get_camera().start_recording()
    assert  watchdog.get_camera().is_recording()
    
    watchdog.watch(1, disks_to_watch=['/a'])
    watchdog.set_watchdog_triggered_interval(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    watchdog.get_system().set_disks_usage([{'mountpoint':'/', 'percent' : 90}])
    time.sleep(2)
    
    assert not watchdog.is_triggered()
    assert watchdog.get_camera().is_recording()
    
    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    assert not watchdog.is_triggered()


def test_one_disk_of_two_percent_over_limit(watchdog: ActionPiWatchdog):
    watchdog.get_camera().start_recording()
    assert  watchdog.get_camera().is_recording()
    
    watchdog.watch(1, disks_to_watch=['/', '/a'])
    watchdog.set_watchdog_triggered_interval(1)
    time.sleep(2)

    assert not watchdog.is_triggered()

    watchdog.get_system().set_disks_usage([{'mountpoint':'/', 'percent' : 10}, {'mountpoint':'/a', 'percent' : 90}])
    time.sleep(2)
    
    assert watchdog.is_triggered()
    assert not  watchdog.get_camera().is_recording()

    watchdog.get_system().set_disks_usage([{'mountpoint':'/', 'percent' : 10}, {'mountpoint':'/a', 'percent' : 20}])
    time.sleep(2)
    
    assert not watchdog.is_triggered()
    assert watchdog.get_camera().is_recording()
    
    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
    assert not watchdog.is_triggered()

def test_cpu_temperature_over_limit(watchdog: ActionPiWatchdog):
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

def test_multiple_unwatch(watchdog: ActionPiWatchdog):

    assert not watchdog.is_watching()
    
    watchdog.unwatch()
    watchdog.unwatch()
    watchdog.unwatch()
    watchdog.unwatch()

    assert not watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()
def test_multiple_watch(watchdog: ActionPiWatchdog):
    watchdog.watch(1)
    watchdog.watch(1)
    watchdog.watch(1)
    watchdog.watch(1)

    assert watchdog.is_watching()

    watchdog.unwatch()
    time.sleep(2)
    assert not watchdog.is_watching()

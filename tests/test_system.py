import pytest

from actionpi.imp.mock import MockSystem

@pytest.fixture
def mock_system():
    return MockSystem()


def test_get_disks_usage(mock_system: MockSystem):
    assert [{'mountpoint':'/', 'percent' : 10}] == mock_system.get_disks_usage()

    mock_system.set_disks_usage([{'mountpoint':'/', 'percent' : 10}, {'mountpoint':'/a', 'percent' : 20}])

    assert [{'mountpoint':'/', 'percent' : 10}, {'mountpoint':'/a', 'percent' : 20}] == mock_system.get_disks_usage()
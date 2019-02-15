import pytest

from mocks.mock_system import MockSystem

@pytest.fixture
def mock_system():
    return MockSystem()


def test_get_disks_usage(mock_system: MockSystem):
    assert {'/' : 10} == mock_system.get_disks_usage()

    mock_system.set_disks_usage({'/' : 10, '/a' : 20})

    assert {'/' : 10, '/a' : 20} == mock_system.get_disks_usage()
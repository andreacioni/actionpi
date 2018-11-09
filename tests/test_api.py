import pytest

from actionpi import ActionPiAPI
from mocks.mock_camera import MockCamera

@pytest.fixture
def api_object():
    camera = MockCamera()
    return ActionPiAPI(camera, "localhost", 8080)

def test_start_and_stop(api_object: ActionPiAPI):
    assert True



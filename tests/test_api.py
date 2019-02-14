import pytest

from flask import jsonify
from flask.json import dumps, loads
from flask.testing import FlaskClient
from actionpi import ActionPiAPI, name, version
from mocks.mock_camera import MockCamera
from mocks.mock_system import MockSystem

@pytest.fixture
def test_client():
    camera = MockCamera()
    system = MockSystem()
    flask_app = ActionPiAPI(camera, system, 'localhost', 8080)
    testing_client = flask_app.get_test_client()
    ctx = flask_app.get_context()
    ctx.push()
 
    yield testing_client
 
    ctx.pop()

def test_render_template(test_client: FlaskClient):
    response = test_client.get('/')

    assert bytes(name, 'utf8') in response.data
    assert bytes(version, 'utf8') in response.data
    assert b'Recording' in response.data
    assert b'Status' in response.data

def test_status(test_client: FlaskClient):
    response = test_client.get('/api/status')

    assert response.status_code == 200
    
    expectedJSON = dumps({
            'system': {
                'cpu_temperature': 20,
                'cpu_load': 33,
                'mem_usage': 60,
                'disk_usage': {'/' : 10}
            }, 
            'recording': False,
            'framerate': 20
        })
    assert loads(expectedJSON) == loads(response.data)

def test_start_stop_recording(test_client: FlaskClient):
    response = test_client.get('/api/start')

    assert response.status_code == 204

    response = test_client.get('/api/stop')

    assert response.status_code == 204


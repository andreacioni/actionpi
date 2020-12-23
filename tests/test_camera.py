import pytest
import time

from os import listdir, path, remove

from actionpi.imp.mock import MockCamera

def create_video_file(index: int, size=1):
    with open('./video.{}.h264'.format(index), 'wb') as f:
        f.seek(size)
        f.write('0'.encode())

@pytest.fixture(autouse=True)
def delete_all_h264_files():
    video_files = [f for f in listdir('.') if f.endswith('.h264')]

    for f in video_files:
        print('Removing: {}'.format(f))
        remove(path.join('.', f))

def test_2_rolling_files():
    max_roll_num = 2
    max_roll_size = 10
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 1)
    
    create_video_file(1, size=max_roll_size + 2)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 2)

    create_video_file(1, size=max_roll_size + 2)
    create_video_file(2, size=max_roll_size - 2)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 2)
    
    create_video_file(1, size=max_roll_size + 2)
    create_video_file(2, size=max_roll_size + 4)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 1)

def test_3_rolling_files():
    max_roll_num = 3
    max_roll_size = 10
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 1)
    
    create_video_file(1, size=max_roll_size + 2)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 2)

    create_video_file(1, size=max_roll_size + 2)
    create_video_file(2, size=max_roll_size - 2)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 2)
    
    create_video_file(1, size=max_roll_size + 2)
    create_video_file(2, size=max_roll_size + 4)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 3)

    create_video_file(1, size=max_roll_size + 2)
    create_video_file(2, size=max_roll_size + 4)
    create_video_file(3, size=max_roll_size + 4)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 1)

    create_video_file(1, size=max_roll_size - 2)
    create_video_file(2, size=max_roll_size + 4)
    create_video_file(3, size=max_roll_size - 4)
    assert (MockCamera(max_roll_size, max_roll_num).get_rolling_number() == 3)

def test_auto_increment():
    max_roll_num = 3
    max_roll_size = 10
    mock_camera = MockCamera(max_roll_size, max_roll_num)

    assert (mock_camera.get_rolling_number() == 1)
    
    create_video_file(1, size=max_roll_size + 2)
    mock_camera.start_recording()
    time.sleep(12)
    
    assert (mock_camera.get_rolling_number() == 2)

    create_video_file(2, size=max_roll_size + 2)
    time.sleep(12)
    
    assert (mock_camera.get_rolling_number() == 3)

    create_video_file(3, size=max_roll_size + 2)
    time.sleep(12)
    
    assert (mock_camera.get_rolling_number() == 1)

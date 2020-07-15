import logging
import re

from os import path, listdir, lstat
from io import BytesIO
from abc import ABC, abstractmethod
from threading import RLock


class AbstractCamera(ABC):

    def __init__(self, width: int, heigth: int, fps: int, rotation: int, output_dir: str, rolling_size=0, rolling_nums=0):
        if rolling_size > 0:
            if rolling_nums < 2:
                raise ValueError('rolling_nums must be greater then 1')

            self._rolling_size = rolling_size
            self._rolling_nums = rolling_nums
            self._is_rolling_rec = True
        else:
            self._is_rolling_rec = False

        self._lock = RLock()

        self._width = width
        self._heigth = heigth
        self._fps = fps
        self._rotation = rotation
        self._output_dir = output_dir

        if self._is_rolling_rec == False:
            self._output_file = path.join(output_dir, 'video.h264')
        else:
            # We increase the rolling file number to prevent accidental ovewrite on restart
            self._current_rolling_file_number = (
                self._evaluate_rolling_file_number(output_dir) + 1) % rolling_nums
            self._output_file = path.join(
                output_dir, 'video.{}.h264'.format(self._current_rolling_file_number))

        self._camera = None

    def _evaluate_rolling_file_number(self, output_dir: str) -> int:
        search_regex = 'video.([1-9][0-9]*).h264'
        video_files = [f for f in listdir(output_dir) if re.search(search_regex, f)]

        if len(video_files) == 0:
            return 1
        
        # Sort videos by dates
        video_files.sort(key=lambda f: lstat(path.join(output_dir, f).st_mtime))

        # Get the number of most recent video
        match = re.search(search_regex, video_files[0])

        return int(match.group(1))

    def get_output_dir(self) -> str:
        return self._output_dir

    def start_recording(self):
        logging.info('Recording %ix%i (%i FPS, rotation: %i) video to %s',
                     self._width, self._heigth, self._fps, self._rotation, self._output_file)
        with self._lock:
            self._start()

    def change_framerate(self, fps: int):
        logging.debug('Changing FPS to %i', fps)
        with self._lock:
            self.stop_recording()
            self._fps = fps
            self.start_recording()

    def stop_recording(self):
        logging.info('Stopping recording')
        with self._lock:
            self._stop()

    def is_recording(self) -> bool:
        with self._lock:
            return self._recording()

    def get_framerate(self) -> int:
        with self._lock:
            return self._fps

    @abstractmethod
    def capture_frame(self) -> BytesIO:
        pass

    @abstractmethod
    def set_led_status(self, status: bool):
        pass

    @abstractmethod
    def _start(self):
        pass

    @abstractmethod
    def _stop(self):
        pass

    @abstractmethod
    def _recording(self) -> bool:
        pass

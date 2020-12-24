import logging
import re
import time
import os

from os import path, listdir, stat
from io import BytesIO
from abc import ABC, abstractmethod
from threading import RLock, Thread, Event
from flask.app import Config

ROLLING_FILE_SIZE_WATCHER_INTERVAL_SEC=10
ROLLING_FILE_SIZE_SEARCH_REGEX = 'video.([1-9][0-9]*).h264'

class AbstractCamera(ABC):

    def __init__(self, config: Config):
        self._config = config
        
        if config['ROTATING_VIDEO_SIZE'] > 0:
            if config['ROTATING_VIDEO_COUNT'] < 2:
                raise ValueError('ROTATING_VIDEO_COUNT must be greater then 1')
            
            self._rolling_nums = config['ROTATING_VIDEO_COUNT']
            self._stop_scheduler = Event()
            self._is_rolling_rec = True
        else:
            self._is_rolling_rec = False
            self._first_run = True

        self._lock = RLock()
        
        self._video_file = None

        if self._is_rolling_rec == False:
            self._output_file = path.join(config['OUTPUT_DIR'], 'video.h264')
        else:
            self._current_rolling_file_number = self._evaluate_first_rolling_file_number(config['OUTPUT_DIR'], config['ROTATING_VIDEO_COUNT'], config['ROTATING_VIDEO_SIZE']) 
            logging.info("Calculated rolling file number: {}".format(self._current_rolling_file_number))            
            self._output_file = path.join(config['OUTPUT_DIR'], 'video.{}.h264'.format(self._current_rolling_file_number))
        
        self._camera = None

    def _start_rolling_files_watcher(self):
        class ScheduleThread(Thread):
            @classmethod
            def run(cls):
                while not self._stop_scheduler.wait(ROLLING_FILE_SIZE_WATCHER_INTERVAL_SEC):
                    with self._lock:
                        file_size = stat(self._output_file).st_size
                        if file_size > self._config['ROTATING_VIDEO_SIZE']:
                            logging.info("File size limit reached for: {} (size: {})".format(self._output_file, file_size))
                            
                            if self._current_rolling_file_number == self._config['ROTATING_VIDEO_COUNT']:
                                logging.info("Reached the maximum number of rolling videos ({}). Restart by one.".format(self._config['ROTATING_VIDEO_COUNT']))
                                self._current_rolling_file_number = 1
                            else:
                                logging.info("Maximum number of video files is not reached. Creating new file, index: {}".format(self._current_rolling_file_number + 1))
                                self._current_rolling_file_number = self._current_rolling_file_number + 1
                            
                            self._output_file = path.join(self._config['OUTPUT_DIR'], 'video.{}.h264'.format(self._current_rolling_file_number))

                            if self._support_split():
                                logging.debug("Split is supported")
                                self._video_file = self._open_video_file_trunc(self._output_file)
                                self._split_recording()
                            else:
                                logging.debug("Split is NOT supported")
                                self._stop()
                                self._video_file.close()
                                self._video_file = self._open_video_file_trunc(self._output_file)
                                self._start()

                
                self._stop_scheduler.clear()

        ScheduleThread().start()

    def _evaluate_first_rolling_file_number(self, output_dir: str, rolling_nums: int, rolling_size: int) -> int:        
        # Get files that match the pattern 
        video_files = [f for f in listdir(output_dir) if re.search(ROLLING_FILE_SIZE_SEARCH_REGEX, f)]
        number_of_files = len(video_files)
        
        if number_of_files == 0:
            logging.info("No uncompleted rolling files exists, let's start with one")
            return 1
        
        # Get only files that have a size lower than `rolling_size`
        video_files = [f for f in video_files if stat(path.join(output_dir, f)).st_size < rolling_size]
        
        if len(video_files) == 0:
            if number_of_files == rolling_nums:
                logging.info("Reached the maximum number of rolling videos ({}). Restart by one.".format(rolling_nums))
                return 1
            
            logging.info("Maximum number of video files is not reached. Creating new file, index: {}".format(number_of_files + 1))
            return number_of_files + 1
        else:
            logging.debug("There are {} video files (out of {}) that are not fully filled".format(len(video_files), number_of_files))
            
            # Map indexes
            video_indexes = [ int(re.search(ROLLING_FILE_SIZE_SEARCH_REGEX, f).group(1)) for f in video_files]
            
            # Get the highest value to avoid deleting recent recordings
            return max(video_indexes)
    
    def _open_video_file_trunc(self, output_file):
        fd = os.open(output_file, flags=os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_SYNC)
        if fd != -1:
            self._first_run = False
            return open(fd, 'wb', buffering=0)
        else:
            raise OSError()

    def _open_video_file_append(self, output_file):
        fd = os.open(output_file, flags=os.O_RDWR|os.O_CREAT|os.O_APPEND|os.O_SYNC)
        if fd != -1:
            return open(fd, 'ab', buffering=0)
        else:
            raise OSError()

    def get_output_dir(self) -> str:
        return self._config['OUTPUT_DIR']

    def start_recording(self):
        logging.info('Recording %ix%i (%i FPS, rotation: %i) video to %s',
                     self._config['WIDTH'], self._config['HEIGHT'], self._config['FRAMERATE'], self._config['ROTATION'], self._output_file)
        with self._lock:
            if(self._is_rolling_rec == True):
                self._start_rolling_files_watcher()
                self._video_file = self._open_video_file_append(self._output_file)
            else:
                if self._first_run:
                    self._video_file = self._open_video_file_trunc(self._output_file)
                else:
                    self._video_file = self._open_video_file_append(self._output_file)
            
            logging.debug(self._video_file)
            
            self._start()

    def change_framerate(self, fps: int):
        logging.debug('Changing FPS to %i', fps)
        with self._lock:
            self.stop_recording()
            self._config['FRAMERATE'] = fps
            self.start_recording()

    def stop_recording(self):
        logging.info('Stopping recording')
        with self._lock:
            if(self._is_rolling_rec == True):
                logging.debug('Terminating rolling files dir watcher...')
                self._stop_scheduler.set()
                while self._stop_scheduler.is_set():
                    time.sleep(2)
                logging.debug('Terminated!')
            self._stop()
            if(self._video_file != None):
                self._video_file.close()

    def is_recording(self) -> bool:
        with self._lock:
            return self._recording()

    def get_framerate(self) -> int:
        with self._lock:
            return self._config['FRAMERATE']
    
    def get_rolling_number(self) -> int:
        if self._is_rolling_rec:
            return self._current_rolling_file_number
        
        return -1

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

    @abstractmethod
    def _support_split(self) -> bool:
        pass

    @abstractmethod
    def _split_recording(self):
        """
        If supported, allows to automatically switch the current output to another one without loosing any frame
        """
        pass

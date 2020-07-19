from io import BytesIO
from actionpi import AbstractCamera

class MockCamera(AbstractCamera):

    def __init__(self, rolling_size=0, rolling_num=0):
        super(MockCamera, self).__init__(1024, 768, 20, 0, ".", rolling_size, rolling_num)
        self.__recording = False

    def _start(self):
        self.__recording = True

    def _stop(self):
        self.__recording = False

    def _recording(self) -> bool:
        return self.__recording

    def capture_frame(self):
        if self.__recording == True:
            buff = BytesIO(b'1234567890')
            buff.seek(0)
            return buff
    
    def set_led_status(self):
        pass

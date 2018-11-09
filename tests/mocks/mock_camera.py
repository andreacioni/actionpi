from actionpi import AbstractCamera

class MockCamera(AbstractCamera):

    def __init__(self):
        super(MockCamera, self).__init__()
        self.__recording = False

    def _start(self):
        self.__recording = True

    def _stop(self):
        self.__recording = False

    def _recording(self) -> bool:
        return self.__recording
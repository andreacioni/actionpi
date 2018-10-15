try:
    from gpiozero import Button
except ImportError:
    raise RuntimeError("not a Raspbian image")


class ActionPiIO(object):

    def __init__(self, gpio):
        self.button = Button(gpio)
    
    def run(self):
        pass
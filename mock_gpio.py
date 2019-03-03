class GPIO_(object):
    BOARD = None
    OUT = None
    HIGH = None
    LOW = None
    def setup(self, pin, mode):
        pass
    def output(self, pin, bool_):
        pass
    def setmode(self, board_type):
        pass
    def PWM(self, pin, freq):
        return PWM_()

GPIO = GPIO_()

class PWM_(object):
    def start(self, int_):
        pass
    def ChangeDutyCycle(self, int_):
        pass

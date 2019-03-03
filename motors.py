import RPi.GPIO as GPIO
from time import sleep

class MotorDriver(object):

    def write_angle(self, servo_pin, servo_pwm, angle):
        duty = angle / 18 + 2 # TODO calibrate function
        GPIO.output(servo_pin, True)
        servo_pwm.ChangeDutyCycle(duty)

        sleep(.5)

        GPIO.output(servo_pin, False)
        servo_pwm.ChangeDutyCycle(0)


    def write_pin_high(self, num_seconds):
        # TODO how does driving backwards work?
        GPIO.output(self.PIN_SHOOT, GPIO.HIGH)
        sleep(num_seconds)
        GPIO.output(self.PIN_SHOOT, GPIO.LOW)



class Driver(MotorDriver):

    PIN_FORWARD = 24 # TODO check
    PIN_BACKWARD = 25 # TODO check
    PIN_LEFT = 26 # TODO check
    PIN_RIGHT = 27 # TODO check

    def __init__(self):
        # Setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_FORWARD, GPIO.OUT)
        GPIO.setup(self.PIN_BACKWARD, GPIO.OUT)
        GPIO.setup(self.PIN_LEFT, GPIO.OUT)
        GPIO.setup(self.PIN_RIGHT, GPIO.OUT)


    # dir=0 is neutral, dir=1 is left, dir=2 is right
    def drive(self, direction, num_seconds, backwards=False):
        with ThreadPoolExecutor(max_workers=4) as executor:
            if not backwards:
                task1 = executor.submit(self.write_pin_high, PIN_FORWARD, num_seconds)
            else:
                task1 = executor.submit(self.write_pin_high, PIN_BACKWARD, num_seconds)

            if direction == 1:
                task2 = executor.submit(self.write_pin_high, PIN_LEFT, num_seconds)
            elif direction == 2:
                task2 = executor.submit(self.write_pin_high, PIN_RIGHT, num_seconds)
            else:
                task2 = None

            task1.result()
            dummy = task2.result() if task2 else None


class Shooter(MotorDriver):

    PIN_PAN = 12
    PIN_TILT = 16
    PIN_SHOOT = 18 # TODO check pins

    pwm_pan = GPIO.PWM(PIN_PAN, 50) # TODO is Ghz right?
    pwm_tilt = GPIO.PWM(PIN_TILT, 50) # TODO ""


    def __init__(self):
        # Setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_PAN, GPIO.OUT)
        GPIO.setup(self.PIN_TILT, GPIO.OUT)
        GPIO.setup(self.PIN_SHOOT, GPIO.OUT)

        pwm_pan.start(0)
        pwm_tilt.start(0)


    def aim_turret(self, x_deg, y_deg):
        with ThreadPoolExecutor(max_workers=4) as executor:
            task1 = executor.submit(write_angle, self.PIN_PAN, self.pwm_pan, x_deg)
            task2 = executor.submit(write_angle, self.PIN_TILT, self.pwm_tilt, y_deg)

            task1.result()
            task2.result()


    def shoot(self, num_seconds):
        write_pin_high(self.PIN_SHOOT, num_seconds)


    def aim_and_shoot(self, x_deg, y_deg, num_seconds):
        self.aim_turret(x_deg, y_deg)
        self.shoot(num_seconds)

    aim_and_shoot(90, 90, 2)

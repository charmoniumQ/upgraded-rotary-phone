import RPi.GPIO as GPIO
from time import sleep

PIN_PAN = 12
PIN_TILT = 16
PIN_SHOOT = 18 # TODO check pins

# Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_PAN, GPIO.OUT)
GPIO.setup(PIN_TILT, GPIO.OUT)
GPIO.setup(PIN_SHOOT, GPIO.OUT)

pwm_pan = GPIO.PWM(PIN_PAN, 50) # TODO is Ghz right?
pwm_tilt = GPIO.PWM(PIN_TILT, 50) # TODO ""

pwm_pan.start(0)
pwm_tilt.start(0)

def write_angle_begin(servo_pin, servo_pwm, angle):
    duty = angle / 18 + 2 # TODO calibrate function
    GPIO.output(servo_pin, True)
    servo_pwm.ChangeDutyCycle(duty)


def write_angle_end(servo_pin, servo_pwm):
    GPIO.output(servo_pin, False)
    servo_pwm.ChangeDutyCycle(0)


def aim_turret(x_deg, y_deg):
    write_angle_begin(PIN_PAN, pwm_pan, x_deg)
    write_angle_begin(PIN_TILT, pwm_tilt, y_deg)

    sleep(1) # TODO this can probably be lowered

    write_angle_end(PIN_PAN, pwm_pan)
    write_angle_end(PIN_TILT, pwm_tilt)

def shoot(num_seconds):
    GPIO.output(PIN_SHOOT, GPIO.HIGH)
    print("starting")
    sleep(num_seconds)
    print("ending")
    GPIO.output(PIN_SHOOT, GPIO.LOW)

def aim_and_shoot(x_deg, y_deg, num_seconds):
    aim_turret(x_deg, y_deg)
    shoot(num_seconds)

aim_and_shoot(90, 90, 2)

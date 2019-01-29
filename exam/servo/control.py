import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03,50)
pwm.start(0)


def setAngle(angle, pwm):
    duty = angle /18 + 2
    GPIO.output(03,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(03,False)
    pwm.ChangeDutyCycle(0)

setAngle(90,pwm)

pwm.stop()
GPIO.cleanup()

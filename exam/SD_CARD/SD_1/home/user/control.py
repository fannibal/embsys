import RPi.GPIO as GPIO
from time import sleep

def setAngle(pwm,angle):
    duty = 20
    GPIO.output(03,True)
    pwm.ChangeDutyCycle(duty)
    sleep(2)
    GPIO.output(03,False)
    pwm.ChangeDutyCycle(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03,50)
pwm.start(0)
sleep(1)            
setAngle(pwm,45)
          
pwm.stop()    
GPIO.cleanup()


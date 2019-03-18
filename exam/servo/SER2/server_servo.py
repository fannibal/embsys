import socket
import RPi.GPIO as GPIO
from time import sleep
import time
import signal
import sys

"""
Serveur pour le servomoteur
"""

#signal handler
def signal_handler(sig, frame):
	print("fin du programme serveur_servo")
	sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


#variables liees au serveur
TCP_IP = '192.168.1.10'
TCP_PORT = 5005
BUFFER_SIZE = 20
t0 = time.time()

#configuration des GPIO et initialisation du PWM
GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03,50)
pwm.start(0)


def setAngle(duty, pwm):
    #duty = angle /18 + 2
    GPIO.output(03,True)
    pwm.ChangeDutyCycle(duty*1.0)
    sleep(1)
    GPIO.output(03,False)
    pwm.ChangeDutyCycle(0*1.0)






#initialisation des sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',TCP_PORT))
t_int = time.time()

while t_int <= t0 + 120: #deux minutes
    print("server launched")
    s.listen(9999)
    conn, addr = s.accept()
    print("Connection address:", addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        try:
            print("received data:", data)
            d = float(data)
            setAngle(d,pwm)
        except:
            pass

    t_int = time.time()
conn.close()
pwm.stop()
GPIO.cleanup()
print("Done")

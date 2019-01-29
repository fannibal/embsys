import socket
import RPi.GPIO as GPIO
from time import sleep

#variables liées au serveur
TCP_IP = '192.168.1.12'
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
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(03,False)
    pwm.ChangeDutyCycle(0)






#initialisation des sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP,TCP_PORT))
t_int = time.time()

while t_int <= t0 + 120: #deux minutes pour l'instant
    s.listen(1)

    conn, addr = s.accept()
    print("Connection address:", addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print("received data:", data)
        setAngle(data,pwm)

        conn.send(data) #conn.send(True) ?
    t_int = time.time()
conn.close()
pwm.stop()
GPIO.cleanup()

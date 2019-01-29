#!/usr/bin/env python
    
import socket
import random
import sys
from threading import Thread, RLock
import time
    
IP_CAM = '192.168.1.10'
PORT_CAM = 5005
IP_SERVO = '192.168.1.12'
PORT_SERVO = 5005
BUFFER_SIZE = 1024

verrou = RLock()
   
class Client(Thread):

    def __init__(self, flag, IP, PORT):
        Thread.__init__(self)
        self.flag = flag
        self.IP = IP
        self.PORT = PORT

    def run(self):
        """Code a executer pendant l'execution du thread"""
        if self.flag == 0: #camera
            pass
        elif self.flag == 1: #servomoteur
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.IP, self.PORT))
            while s.recv(BUFFER_SIZE)!= "end":
                print "Connection on {}".format(self.PORT)
                m = input(">> ")
                s.send(m.encode())
            s.close()

            print "received data:", data
   
if __name__ == '__main__':
    # Creation des threads
    thread_cam = Client(0,IP_CAM,PORT_CAM)
    thread_servo = Client(1,IP_SERVO,PORT_SERVO)

    # Lancement des threads
    thread_cam.start()
    thread_servo.start()

    # Attend que les threads se terminent
    thread_cam.join()
    thread_servo.join()
    
    print("Done")
    
    
    

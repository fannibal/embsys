#!/usr/bin/env python
    
import socket
import sys
from threading import Thread, RLock
from tkinter import Tk, Button, Scale, IntVar, HORIZONTAL, Canvas, Label, ttk
from PIL import Image,ImageTk
import signal
from numpy import array,ones,vstack

def signal_handler(sig,frame):
    print("client terminated")
    sys.exit()
signal.signal(signal.SIGINT,signal_handler)
signal.signal(signal.SIGTERM,signal_handler)
    
CAM = 1
SERVO = 0
IP_CAM = '192.168.1.10'
PORT_CAM = 5000
IP_SERVO = '192.168.1.10'
PORT_SERVO = 5005
BUFFER_SIZE = 999999
img_log = []

verrou = RLock()
   
class Client(Thread):

    def __init__(self, flag, IP, PORT,fenetre):
        Thread.__init__(self)
        self.flag = flag
        self.IP = IP
        self.PORT = PORT
        self.fenetre = fenetre

        ### GUI ###
        if self.flag == CAM:
            self.callback = self.callback_cam
        elif self.flag == SERVO:
            self.callback = self.callback_servo
        else:
            print("Not a valid thread")
        self.tab = self.fenetre.winfo_children()[0].winfo_children()[self.flag]
        self.tab.winfo_children()[0].config(command = self.callback)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.IP, self.PORT))
        print("Connection on {}".format(self.PORT))


    def run(self):
        """Code a executer pendant l'execution du thread"""

    def callback_cam(self):
        S = []
        L = []
        
        m = "i"
        print(m.encode())
        self.s.send(m.encode())
        try:
            tmp = self.s.recv(BUFFER_SIZE)
            k = 0
            r = 0
            smax=640*480*3
            while r<= smax and tmp!=b'':
                k+=1
                S.append(tmp)
                r += len(tmp)
                if r < smax:
                    tmp = self.s.recv(BUFFER_SIZE)
            self.tab.winfo_children()[2].config(text="...")
            for string in S:
                for byte in string:
                    L.append(byte)
            nL = array(L[:640*480*3])
            L1,L2,L3 = array(nL[0::3]).reshape((480,-1)),array(nL[1::3]).reshape((480,-1)),array(nL[2::3]).reshape((480,-1))
            L1,L2,L3 = L1*1.0,L2*1.0,L3*1.0 #int to float
            img = ImageTk.PhotoImage(image=Image.fromarray(L1))
            self.tab.winfo_children()[1].create_image(320,240,image=img)
            global img_log
            img_log=img
        except:
            self.tab.winfo_children()[2].config(text="Error, try again")
            
    def close_s(self):
        self.s.close()
   
    def callback_servo(self):
        m = str(self.tab.winfo_children()[1].get())
        self.s.send(m.encode())
   
if __name__ == '__main__':
    ########################################################
    # Creation de la fenetre
    fenetre = Tk()
    fenetre.title("Client")
    tab_control = ttk.Notebook(fenetre)
    # tab pour servomoteur
    tab1 = ttk.Frame(tab_control)
    b1 = Button(tab1, text = "send angle", command = None) #command change dans la thread correspondante
    b1.grid()
    s1 = Scale(tab1, variable = IntVar(), orient = HORIZONTAL, to=180)
    s1.grid()
    # tab pour camera
    tab2 = ttk.Frame(tab_control)
    b2 = Button(tab2, text = "get image", command = None) #command change dans la thread correspondante
    b2.grid()
    c2 = Canvas(tab2,bg="black",height=480,width=640)
    c2.grid()
    l2 = Label(tab2,text="...")
    l2.grid()
    # finalisation fenetre
    tab_control.add(tab1,text="servomoteur")
    tab_control.add(tab2,text="camera")
    tab_control.pack(expand=1,fill='both')
    ########################################################
    # Creation des threads
    thread_cam = Client(CAM,IP_CAM,PORT_CAM,fenetre)
    thread_servo = Client(SERVO,IP_SERVO,PORT_SERVO,fenetre)

    # Lancement des threads
    thread_cam.start()
    thread_servo.start()

    fenetre.mainloop()
    print("GUI done")
    thread_cam.close_s()
    thread_servo.close_s()
    # Attend que les threads se terminent
    thread_cam.join()
    thread_servo.join()
    ########################################################
    
    print("end of code")
    
    
    

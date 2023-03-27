import socket
import random as r
import time
#import broker2
# import server1
import os
from pathlib import Path
#import subprocess 
import sys
from subprocess import Popen, CREATE_NEW_CONSOLE

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((socket.gethostname(), 1001))
serv.settimeout(22)
serv.listen(5)
print("Waiting client to be connected")

count1 = 0

while True:
    while True:
        try:
            conn, addr = serv.accept()
            from_client = ''
            print("hi")
            count1+=1
            while True:  
                data = conn.recv(1024)
                print(data)
                if not data: 
                    break
                n = data.decode('utf-8')
                b=n.encode('ASCII')
                conn.send(bytes(n, 'utf-8'))
                print(b)
        except:
            if(count1%3==0):
                Popen('python broker2.py', creationflags=CREATE_NEW_CONSOLE)
            elif(count1%3==1):
                Popen('python broker1.py', creationflags=CREATE_NEW_CONSOLE)
            elif(count1%3==2):
                Popen('python broker3.py', creationflags=CREATE_NEW_CONSOLE)

            break
conn.close()


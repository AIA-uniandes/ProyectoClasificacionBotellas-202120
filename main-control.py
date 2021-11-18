
from threading import Thread
import asyncio
import time
import socket

communication=0
state=0
end=False



def setCommunication():
    print('setting communication')

def runState():
    global state

def checkCommunication():
    while not end:
        time.sleep(30)

def connectRobot(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Obligatorio (https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.connect((host, port))


def main():
    global communication
    #get type of communication
    Thread(target=setCommunication, args=[communication]).start()
    Thread(target=checkCommunication).start()

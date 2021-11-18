#!/usr/bin/env python3
import os
import socket
from threading import Thread
import asyncio
import time
import socket
from robotMove.robotControl import *
import audioProcess.grabar as rec
import audioProcess.procesar as pred
# IOT Protocols
import communication.ws as ws

# constants
HOST_R = "157.253.197.6"    #
PORT_R = 30002
HOST_WS = ""
PORT_WS = "8765"


communication = 0
newBottle = False
state = 0
end = False
robot
loop
bands = []


def lab_to_class(label):
    if label == 1:
        return "glass"
    else:
        return "plastic"


def commandRobot(orders):
    global robot
    for ele in orders:
        if ele['type'] == 'trayectory':
            for p in ele['points']:
                com = ("%s(%s, a=%s, v=%s)" % (
                    p['function'], p['coords'], p['a'], p['v']) + "\n").encode("utf8")
                print(com)
                robot.send(com)
                time.sleep(p['time'])
        elif ele['type'] == 'tool':
            com = ("set_digital_out(8,%s)" %
                   ele['value'] + "\n").encode("utf8")
            print(com)
            robot.send(com)
            time.sleep(1.5)
        elif ele['type'] == 'record':
            print("recording")
            # Thread(target=rec.record, args=[os.path.dirname(__file__)+"audioProcess/predictions/pred.wav",1]).start()


def runState():
    global state, newBottle
    if state == 0:
        newBottle = False
        commandRobot(getBottle)
        state = 1
        print("recording")
        Thread(target=rec.record, args=[os.path.dirname(
            __file__)+"audioProcess/predictions/pred.wav", 1]).start()
        commandRobot(kickBottle)
        state = 2
        time.sleep(1.5)
        result = pred.process()
        result = 1
        print(lab_to_class(result))
        commandRobot(finalTrayectories[result])
        state = 3
        commandRobot(getBack)
        state = 0
        if newBottle:
            runState()


def setCommunication(protocol):
    global loop
    print('setting communication')
    if protocol == 0:
        loop = asyncio.get_event_loop().run_until_complete(
            start_server(HOST_WS, PORT_WS, getSMS))


def checkCommunication():
    while not end:
        time.sleep(30)


def connectRobot(host, port):
    global robot
    # Obligatorio (https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/)
    robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    robot.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    robot.connect((host, port))


def main():
    global communication, state, HOST_R, PORT_R
    # get type of communication
    Thread(target=setCommunication, args=[communication]).start()
    Thread(target=checkCommunication).start()

    connectRobot(HOST_R, PORT_R)


async def getSMS(websocket, path):
    global newBottle
    print(path)
    # case to register client
    if path == '/bottle':
        bands.add(websocket)
        try:
            async for msg in websocket:
                print(msg)
                newBottle = True
                runState()
                pass
        finally:
            bands.remove(websocket)

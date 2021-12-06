#!/usr/bin/env python3
import os
import socket
from threading import Thread
import asyncio
import time
import socket
from robotMove.robotControl import *
import audioProcess.grabar as rec
# import audioProcess.procesar as pred
# IOT Protocols
import communication.ws as ws

import urllib.request
import json

# constants
HOST_R = "157.253.197.6"    #
PORT_R = 30002
HOST_WS = ""
PORT_WS = "8765"


communication = 0
newBottle = False
state = 0
end = False
bands = set()
settings={
    'Estado':'On',
    'Protocolo_actual':'MQTT'
}
newUpdate=False

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
                # print(com)
                robot.send(com)
                time.sleep(p['time'])
        elif ele['type'] == 'tool':
            com = ("set_digital_out(8,%s)" %
                   ele['value'] + "\n").encode("utf8")
            # print(com)
            robot.send(com)
            time.sleep(1.5)
        

def runState():
    global state, newBottle,path,bands
    print('Current bottle')
    print(newBottle)
    if state == 0:
        state = 1
        newBottle = False
        commandRobot(getBottle)
        state = 2
        commandRobot(takePosition)
        print("recording")
        Thread(target=rec.record, args=[os.path.dirname(
            path)+"audioProcess/predictions/pred.wav", 1]).start()
        time.sleep(0.3)    
        commandRobot(kickBottle)
        state = 3
        time.sleep(1.5)
        # result = pred.process(os.path.dirname(
        #     path)+"audioProcess")
        result = 1
        print(lab_to_class(result))
        commandRobot(finalTrayectories[result])
        state = 4
        commandRobot(openTool)
        commandRobot(getBack)
        state = 0
        print("finish have botte")
        print(newBottle)
        if newBottle:
            runState()


def setCommunication(protocol):
    global loop, wsServer
    print('setting communication')
    if protocol == 0:
        l = asyncio.new_event_loop()
        asyncio.set_event_loop(l)
        loop=l
        wsServer = l.run_until_complete(
            ws.startServer(HOST_WS, PORT_WS, getSMS))
        l.run_forever()

def checkCommunication():
    global loop, bands
    while not end:
        c = urllib.request.urlopen("https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/tesis-app-zayvx/service/Control/incoming_webhook/control").read()
        # c='[{\"_id\":\"617c297ebd1ea69c6b80d218\",\"opcion1\":\"Turn On\",\"opcion2\":\"Turn Off\",\"Estado\":\"On\",\"Protocolo_actual\":\"MQTT\",\"protocolo1\":\"MQTT\",\"protocolo2\":\"WEB SOCKETS\",\"protocolo3\":\"COAP\"}]'
        c=json.loads(c)
        contents=json.loads(c)
        if not contents[0]['Estado'] == settings['Estado'] or not contents[0]['Protocolo_actual'] == settings['Protocolo_actual']:
            print("change")
            print(loop)
            print(contents[0])
            loop.call_soon_threadsafe(ws.broadcast,'change',bands)
            settings['Estado']= contents[0]['Estado']
            settings['Protocolo_actual']= contents[0]['Protocolo_actual']
        time.sleep(30)


def connectRobot(host, port):
    global robot
    # Obligatorio (https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/)
    robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    robot.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    robot.connect((host, port))
    commandRobot(goInit)



def main():
    global communication, state, HOST_R, PORT_R,path

    path = __file__
    # get type of communication
    # connectRobot(HOST_R, PORT_R)
    Thread(target=setCommunication, args=[communication]).start()
    Thread(target=checkCommunication).start()


async def getSMS(websocket, path):
    global newBottle, bands, state
    Thread(target=checkCommunication).start()
    print('new Conection')
    print(path)
    # case to register client
    if path == '/bottle':
        bands.add(websocket)
        print(type(websocket))
        try:
            async for msg in websocket:
                print(msg)
                if not state ==1:
                    newBottle = True
                    Thread(target=runState).start()
                pass
        finally:
            bands.remove(websocket)
main()

#!/usr/bin/env python3
import os
from threading import Thread
import asyncio
import time
import socket
import aiocoap.resource as resource
import aiocoap

# Local imports
from robotMove.robotControl import *
# import audioProcess.grabar as rec
# import audioProcess.procesar as pred
# IOT Protocols
import communication.ws as ws
import communication.mqtt as mqtt
import communication.coap as coap

import urllib.request
import json

# constants
HOST_R = "157.253.197.6"    #
PORT_R = 30002
HOST_WS = ""
PORT_WS = "8765"
HOST_MQTT = ""
PORT_MQTT = "1884"


communication = 0
newBottle = False
state = 0
end = False
bands = set()
settings = {
    'Estado': 'On',
    'Protocolo_actual': 'MQTT'
}
newUpdate = False


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
    global state, newBottle, path, bands
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
        loop = l
        wsServer = l.run_until_complete(
            ws.startServer(HOST_WS, PORT_WS, getMsgWS))
        l.run_forever()
    elif protocol == 1:
        mqtt.connect(HOST_MQTT, PORT_MQTT, getMsgMQTT)
    elif protocol == 2:
        coap.server(msgCOAP)


def checkCommunication():
    global loop, bands
    while not end:
        c = urllib.request.urlopen(
            "https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/tesis-app-zayvx/service/Control/incoming_webhook/control").read()
        # c='[{\"_id\":\"617c297ebd1ea69c6b80d218\",\"opcion1\":\"Turn On\",\"opcion2\":\"Turn Off\",\"Estado\":\"On\",\"Protocolo_actual\":\"MQTT\",\"protocolo1\":\"MQTT\",\"protocolo2\":\"WEB SOCKETS\",\"protocolo3\":\"COAP\"}]'
        c = json.loads(c)
        contents = json.loads(c)
        if not contents[0]['Estado'] == settings['Estado'] or not contents[0]['Protocolo_actual'] == settings['Protocolo_actual']:
            print("change")
            # print(contents[0])
            # loop.call_soon_threadsafe(ws.broadcast, 'change', bands)
            settings['Estado'] = contents[0]['Estado']
            settings['Protocolo_actual'] = contents[0]['Protocolo_actual']
        time.sleep(30)


def connectRobot(host, port):
    global robot
    # Obligatorio (https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/)
    robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    robot.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    robot.connect((host, port))
    commandRobot(goInit)


def main():
    global communication, state, HOST_R, PORT_R, path

    path = __file__
    # get type of communication
    # connectRobot(HOST_R, PORT_R)
    Thread(target=setCommunication, args=[communication]).start()
    Thread(target=checkCommunication).start()


async def getMsgWS(websocket, path):
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
                processMessage(msg)
                pass
        finally:
            bands.remove(websocket)


def getMsgMQTT(client, userdata, msg):
    processMessage(msg)


class msgCOAP(resource.Resource):
    async def render_put(self, request):
        processMessage(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload="get message")


def processMessage(msg):
    global newBottle, state, bands
    print(msg)
    millis = int(round(time.time() * 1000))
    # extrae la informacion del mensaje
    data = json.loads(msg.payload.decode("utf-8"))
    print('time: '+str(millis-data['time']))
    print(data)
    if not state == 1:
        newBottle = True

        # Thread(target=runState).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # quit
        os.system.exit()

import asyncio
import websockets
import paho.mqtt.publish as publish
from aiocoap import *
import time
import json
from threading import Thread

host = "localhost"


async def connect():
    global current, initial, ws
    # create the url to connect the server
    uri = "ws://"+host+":8765/bottle"
    # Create the websocket
    ws = await websockets.connect(uri)
    async for msg in ws:
        print(msg)


async def sendWS(data):
    global ws
    await ws.send(data)


async def sendCOAP(data):

    context = await Context.create_client_context()
    request = Message(code=PUT, payload=data, uri="coap://"+host+"/bottle")

    # response = await context.request(request).response

    # print('Result: %s\n%r' % (response.code, response.payload))


def test(protocol):
    while True:
        data = {
            'time': int(round(time.time() * 1000)),
            'data': "llego botella"
        }
        # pass to json
        data = json.dumps(data)
        if protocol == 0:
            asyncio.run(sendWS(data))
        elif protocol == 1:
            print("posting MQTT")
            publish.single("bottle", data, hostname=host, port=1884)
        elif protocol == 2:
            asyncio.run(sendCOAP(data))
        time.sleep(2)


def runAsync():
    l = asyncio.new_event_loop()
    asyncio.set_event_loop(l)
    l.run_until_complete(connect())


# Thread(target=runAsync).start()
time.sleep(2)
test(2)

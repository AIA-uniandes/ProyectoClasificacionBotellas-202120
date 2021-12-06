import asyncio
import websockets
import time
import json
from threading import Thread

a=[5,6,7]
async def ticker():
    """Yield numbers from 0 to `to` every `delay` seconds."""
    while 1: 
        if len(a):
            yield a.pop(0)
        time.sleep(1)


async def connect():
    global current, initial
    #create the url to connect the server
    uri = "ws://localhost:8765/bottle"
    #Create the websocket
    ws = await websockets.connect(uri)
    #First message to register the client 
    # await ws.send('hola')
    # print("waiting")
    async for msg in ws:
       print(msg)

async def test():
    async for msg in ticker():
        print(msg)

def runAsync():
    l = asyncio.new_event_loop()
    asyncio.set_event_loop(l)
    l.run_until_complete(connect())


Thread(target=runAsync).start()
time.sleep(2)

import websockets
import time


async def connect(host, port):
    # create the url to connect the server
    uri = "ws://"+host+":"+port+"/bottle"
    # Create the websocket
    return await websockets.connect(uri)
# Server


async def broadcast(msg, clients):
    for ws in clients:
        await ws.send(msg)


def startServer(host, port, callback):
    print('get server')
    return websockets.serve(callback, host, port)

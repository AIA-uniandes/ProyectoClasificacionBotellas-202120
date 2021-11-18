import websockets
import asyncio
#Client
async def connect(host,port):
    #create the url to connect the server
    uri = "ws://"+host+":"+port+"/recieve"
    #Create the websocket
    return await websockets.connect(uri)
#Server
async def broadcast(msg,clients):
    for ws in clients:
        await ws.send(msg)

def startServer(host,port, callback):
    return websockets.serve(callback, host, port)
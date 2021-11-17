#!/usr/bin/env python3
import os
import socket
#import struct
import time
import struct
import math
# import grabar as rec
# import procesar as pred
from threading import Thread



def angleToRadian(list):
    for i in range(0,len(list)):
        list[i]=list[i]*math.pi/180
    return list
def lab_to_class(label):
    if label==1:
      return "glass"
    else:
      return "plastic"

finalTrayectories=[
    {
        'type': 'trayectory',
        'points':[
            {
                'function':'movej',
                'time':5,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-320,-37.39,30.56,13.47,41.75,130.9])
            },
            {
                'function':'movel',
                'time':2,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-318.92,-25.29,54.3,-30.1,42.6,137.44])
            }
        ]
    },
    {
        'type': 'trayectory',
        'points':[
            {
                'function':'movej',
                'time':5,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-270.34,-56.77,64.14,-2.23,91.73,136.59])
            },
            {
                'function':'movel',
                'time':2,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-270.36,-39.51,81.96,-37.31,91.89,136.52])
            }
        ]
    },
   
]

orders=[
    {
        'type':'tool',
        'value':False
    },
    {
        'type': 'trayectory',
        'points':[
            {
                'function':'movej',
                'time':8.5,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-28.02,-49.3,118.83,-71.74,62.79,137.68])
            },
            {
                'function':'movel',
                'time':1,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-16.91,-23.06,54.16,-33.18,73.77,137.68])
            }
        ]
    },
    {
        'type':'tool',
        'value':True
    },
    {
        'type': 'trayectory',
        'points':[
            {
                'function':'movej',
                'time':8.3,
                'v':0.3,
                'a':1,
                'coords':angleToRadian([-4.62,-64.36,-4.73,97.36,95.2,137.68])
            },
        ]
    },    
    {
        'type': 'record'
    },
    {
        'type': 'trayectory',
        'points':[
            {
                'function':'movej',
                'time':4,
                'v':3.7,
                'a':1.5,
                'coords':angleToRadian([-285,-64.36,-4.73,97.36,95.2,137.68])
            },
        ]
    },
    {
        'type':'predict'
    }
]
print(orders)

#Server creation	
# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.bind(("localhost", 31001))
# serversocket.listen(5) #5 eingehende Verbindungen erlauben

HOST = "157.253.197.6"    # The remote host #Cambiar
PORT = 30002              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Obligatorio (https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.connect((HOST, PORT))

for ele in orders:
    if ele['type'] == 'trayectory':
        for p in ele['points']:
            com = ("%s(%s, a=%s, v=%s)"%(p['function'],p['coords'],p['a'],p['v']) + "\n").encode("utf8")
            print(com)
            s.send(com)
            time.sleep(p['time'])  
    elif ele['type'] == 'tool':
        com =("set_digital_out(8,%s)"%ele['value'] + "\n").encode("utf8")
        print(com)
        s.send (com)
        time.sleep(1.5)
    elif ele['type'] == 'record':
        print("recording")
        # Thread(target=rec.record, args=[os.path.dirname(__file__)+"/predictions/pred.wav",1]).start()
    elif ele['type'] == 'predict':
        # result = pred.process()
        result = 1
        print(lab_to_class(result))
        orders.append(finalTrayectories[result])
        orders.append({
        'type':'tool',
        'value':False
        })
        orders.append({
        'type': 'trayectory',
            'points':[
                {
                    'function':'movej',
                    'time':3,
                    'v':0.3,
                    'a':1,
                    'coords':angleToRadian([-307.71,-56.58,113.3,-54.19,54.03,132.26])
                },
                {
                    'function':'movej',
                    'time':18.5,
                    'v':1,
                    'a':1,
                    'coords':angleToRadian([-28.02,-49.3,118.83,-71.74,62.79,137.68])
                }
            ]  
        })
     
#Para revisar:
# General - https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/
# Posiciones y requests - http://axisnj.com/controlling-a-universal-robots-cobot-using-python/
# 




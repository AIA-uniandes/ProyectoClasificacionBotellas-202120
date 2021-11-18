#!/usr/bin/env python3
import math


def angleToRadian(list):
    for i in range(0, len(list)):
        list[i] = list[i]*math.pi/180
    return list


getBottle = [
    {
        'type': 'tool',
        'value': False
    },
    {
        'type': 'trayectory',
        'points': [
            {
                'function': 'movej',
                'time': 8.5,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-28.02, -49.3, 118.83, -71.74, 62.79, 137.68])
            },
            {
                'function': 'movel',
                'time': 1,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-16.91, -23.06, 54.16, -33.18, 73.77, 137.68])
            }
        ]
    },
    {
        'type': 'tool',
        'value': True
    },
    {
        'type': 'trayectory',
        'points': [
            {
                'function': 'movej',
                'time': 8.3,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-4.62, -64.36, -4.73, 97.36, 95.2, 137.68])
            },
        ]
    }
]


kickBottle = [

    {
        'type': 'record'
    },
    {
        'type': 'trayectory',
        'points': [
            {
                'function': 'movej',
                'time': 4,
                'v': 3.7,
                'a': 1.5,
                'coords': angleToRadian([-285, -64.36, -4.73, 97.36, 95.2, 137.68])
            },
        ]
    }
]

finalTrayectories = [
    [{
        'type': 'trayectory',
        'points': [
            {
                'function': 'movej',
                'time': 5,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-320, -37.39, 30.56, 13.47, 41.75, 130.9])
            },
            {
                'function': 'movel',
                'time': 2,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-318.92, -25.29, 54.3, -30.1, 42.6, 137.44])
            }
        ]
    }],
    [{
        'type': 'trayectory',
        'points': [
            {
                'function': 'movej',
                'time': 5,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-270.34, -56.77, 64.14, -2.23, 91.73, 136.59])
            },
            {
                'function': 'movel',
                'time': 2,
                'v': 0.3,
                'a': 1,
                'coords': angleToRadian([-270.36, -39.51, 81.96, -37.31, 91.89, 136.52])
            }
        ]
    }],
]

getBack = [
    {
        'type': 'trayectory',
                'points': [
                    {
                        'function': 'movej',
                        'time': 3,
                        'v': 0.3,
                        'a': 1,
                        'coords': angleToRadian([-307.71, -56.58, 113.3, -54.19, 54.03, 132.26])
                    },
                    {
                        'function': 'movej',
                        'time': 18.5,
                        'v': 1,
                        'a': 1,
                        'coords': angleToRadian([-28.02, -49.3, 118.83, -71.74, 62.79, 137.68])
                    }
                ]
    }
]

# Para revisar:
# General - https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips-cb2-cb3/index.php/ur-script-send-commands-from-host-pc-to-robot-via-socket-connection/
# Posiciones y requests - http://axisnj.com/controlling-a-universal-robots-cobot-using-python/
#

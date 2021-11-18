#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import asyncio
import websockets
import time
import json

import sys
from threading import Thread
import os
from TouchStyle import *
import ftrobopy
import smbus
#import struct, array, math

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
ws


async def connect(host, port):
    global ws
    # create the url to connect the server
    uri = "ws://"+host+":"+port+"/bottle"
    # Create the websocket
    ws = await websockets.connect(uri)


class TouchGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.win = TouchWindow("Band Controller")
        self.vbox = QVBoxLayout()
        self.vbox.addStretch()

        try:
            # connect to TXT's IO controller
            self.txt = ftrobopy.ftrobopy("localhost", 65000)
        except:
            self.txt = None

        if not self.txt:
            err_msg = QLabel("Error connecting IO server")
            err_msg.setWordWrap(True)
            err_msg.setAlignment(Qt.AlignCenter)
            self.vbox.addWidget(err_msg)
        else:
            M = [self.txt.C_OUTPUT, self.txt.C_OUTPUT,
                 self.txt.C_OUTPUT, self.txt.C_OUTPUT]
            I = [(self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL)]
            self.txt.setConfig(M, I)
            self.txt.updateConfig()
            # set initial values
            self.band_on = True
            self.vel = 4
            self.dir = True
            # initialize ultrasound
            self.ultrasound = self.txt.ultrasonic(1)

            # assume initually the button is not pressed
            self.distance = 0
            self.timer = QTimer(self)  # create a timer
            # connect timer to on_timer slot
            self.timer.timeout.connect(self.on_timer)
            # fire timer every 100ms (10 hz)
            self.timer.start(100)
            self.turn_on()
            # initialize interface
            self.vbox.addStretch()
            self.win.centralWidget.setLayout(self.vbox)
            self.win.show()
            self.exec_()

    def turn_on(self):
        if self.band_on:
            self.move_band()
        else:
            bus.write_byte(0x8, 0x0)

    def revert(self):
        self.dir = not self.dir
        self.move_band()

    def up_v(self):
        if self.vel < 5:
            self.vel = self.vel + 1
            self.move_band()

    def down_v(self):
        if self.vel > 1:
            self.vel = self.vel - 1
            self.move_band()

    def move_band(self):
        if self.dir:
            bus.write_byte(8, hex(6-self.vel))
        else:
            bus.write_byte(8, hex(5+self.vel))

    def on_timer(self):
        # change saved state to reflect input state
        self.distance = self.ultrasound.distance()
        print(self.distance)
        # toggle lamp state if button has been pressed
        # if self.distance > 9 and not self.band_on:
        #     self.band_on = True
        if self.distance < 10 and self.band_on:
            self.band_on = False
            ws.send(True)
        self.turn_on()


def communication():
    asyncio.get_event_loop().run_until_complete(connect())


if __name__ == "__main__":
    Thread(target=communication).start()
    TouchGuiApplication(sys.argv)

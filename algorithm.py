import cv2
from mouseserver import *
from pymouse import PyMouse


class MouseListener(Listener):

    def on_event(self, event):
        type = event[0]
        x = event[1]
        y = event[2]
        print "Type:", type, "at(", x, ",", y, ")"
        if x is not -1 and y is not -1:
            if type is MouseServer.MOUSE_MOVE:
                mouse.move(x, y)
            elif type is MouseServer.MOUSE_DOWN:
                mouse.press(x, y)
            elif type is MouseServer.MOUSE_UP:
                mouse.release(x, y)

    def on_error(self, message):
        print message

mouse = PyMouse()
listener = MouseListener()
mouse_server = MouseServer(cv2.VideoCapture(0), listener)
mouse_server.start()
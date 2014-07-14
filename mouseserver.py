__author__ = 'ruraj'

import cv2
import threading


class MouseServer(threading.Thread):
    #Size of moving window in which to check for toggle
    WINDOW_SIZE = 4
    #States for laser
    LASER_OFF = 1
    LASER_ON = 2
    LASER_TOGGLED = 3
    VERIFY_TOGGLE = 4
    #States for mouse
    MOUSE_UP = 10
    MOUSE_DOWN = 11
    MOUSE_MOVE = 12
    #Hold the current state of laser
    LASER_STATE = LASER_OFF
    #Hold the current state of mouse
    MOUSE_STATE = MOUSE_UP
    #Array of states for moving window
    stateList = []

    def __init__(self, source, eventListener):
        super(MouseServer, self).__init__()
        if not isinstance(eventListener, Listener):
            raise Exception("Error", "Object not of type Listener")

        self.running = True
        self.source = source
        self.eventListener = eventListener
        self.x = self.y = 0

    def run(self):
        while self.running is True:
            ret, frame = self.source.read()
            if frame is None:
                break
            x, y, w, h, state = self.find_laser(frame)

            toggled = self.check_states(state, self.WINDOW_SIZE)

            if self.LASER_STATE == self.LASER_OFF:
                if state is True:
                    self.LASER_STATE = self.LASER_ON
                continue
            elif self.LASER_STATE == self.LASER_ON:
                if toggled is True:
                    self.LASER_STATE = self.LASER_TOGGLED
                pass
            elif self.LASER_STATE == self.LASER_TOGGLED:
                if toggled is not True:
                    temp_state = self.MOUSE_UP
                    self.LASER_STATE = self.LASER_OFF
                else:
                    temp_state = self.MOUSE_DOWN

                if temp_state != self.MOUSE_STATE:
                    self.MOUSE_STATE = temp_state
                    self.eventListener.on_event([self.MOUSE_STATE, self.x, self.y])

            if self.x is x and self.y is y:
                pass
            else:
                self.x = x
                self.y = y
                self.eventListener.on_event([self.MOUSE_MOVE, x, y])
        return

    def check_states(self, state, size):
        if len(self.stateList) > 0:
            self.stateList.pop(0)
        self.stateList.append(state)
        for pState in self.stateList[-(size+2):]:
            if pState != state:
                return True
        return False

    @staticmethod
    def find_laser(frame):
        x = y = w = h = -1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            laser_state = True
            cnt = contours[0]
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.CV_AA)
        else:
            laser_state = False
        cv2.imshow("images", frame)
        key = cv2.waitKey(42)
        if key is ord('q'):
            self.running = False
        return x, y, w, h, laser_state


class Listener(object):

    def on_event(self, event):
        pass

    def on_error(self, message):
        pass
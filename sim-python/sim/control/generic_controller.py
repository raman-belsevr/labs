import sys
import traceback
import pygame
import pygame.locals
import platform
from sim.control.controller_display import ControllerDisplay
from sim.control.dummy_display import DummyDisplay


class GenericController(object):

    END_OF_INPUT = -1

    def __init__(self, name, switch_labels):
        '''
        Creates a new Controller object.
        '''

        # Set constants
        self.BAND = 0.2  # Must be these close to neutral for hold / autopilot

        # Init pygame
        #self.display = ControllerDisplay(name, switch_labels)
        self.display = DummyDisplay(name, switch_labels)


        # Supports keyboard polling
        self.keys = []
        self.name = name
        # not working curently, object not callable
        #self.platform = platform()[0:platform().find('-')]


    def __str__(self):
        '''
        Returns a string representation of this Controller object
        '''
        return self.name

    def _pump(self):
        # pygame.event.pump()
        pass

    def _startup(self):
        return
        if not self.ready:

            self.message(self._startup_message())

            while True:
                self._pump()
                if self._get_throttle() > .5:
                    break

            while True:
                self._pump()
                if self._get_throttle() < .05 and self._get_switchval() == 0:
                    break

            self.clear()

            self.ready = True

    def poll(self):
        self._pump()
        self._startup()

        demands = self._get_pitch(), self._get_roll(), self._get_yaw(), self._get_throttle()
        self._mark_done()
        switchval = self._get_switchval()

        self.display.draw(demands, switchval)
        return demands[0], demands[1], demands[2], demands[3], switchval

    def _mark_done(self):
        pass

    def running(self):
        '''
        Returns True if the QuadStick is running, False otherwise. Run can be terminated by hitting
        ESC.
        '''
        return self.display.running()


    def clear(self):
        '''
        Clears the display.
        '''
        self.display.clear()


    def message(self, msg):
        '''
        Displays a message.
        '''
        self.clear()

        self._display(msg)

    def _display(self, msg):
        self.display.display(msg)

    def _get_axis(self, k):
        return 0

    def _get_button(self, k):
        return 0

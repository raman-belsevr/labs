import pygame
import traceback
import sys


class DummyDisplay:

    def __init__(self, name, switch_labels):
        pass

    def draw(self, demands, switchval):
        pass

    def clear(self):
        '''
        Clears the display.
        '''
        pass

    def error(self):
        '''
        Displays the most recent exception as an error message, and waits for ESC to quit.
        '''
        pass

    def _show_switch(self, switchval, index):
        pass

    def _show_demand(self, demands, index, sign, label):
        pass

    def _draw_label_in_row(self, text, row, color=(255, 255, 255)):
        pass

    def _draw_label(self, text, y, color=(255, 255, 255)):
        pass

    def display(self, msg):
        pass

    def running(self):
        return True
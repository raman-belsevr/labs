from raspi.sensor import sensor_model


"""
Dummy GPIO that simulates actual rasberry-platform compatible code.
RPi.GPIO library is not compatible on other platforms (e.g. Mac)
"""

""" Numbering convention for the Raspi board """
BOARD = 1
BCM = 2

""" Input/Output mode"""
IN = 1
OUT = 2

""" Applied voltage (low/high) """
LOW = 1
HIGH = 2


def setmode(mode):
    print("Set mode to %" % mode)


def setup(pin, mode):
    print("Setting % pin to % mode" % pin, mode)


def output(pin, output_value):
    print("output % to %" % output_value, pin)


def input(pin):
    input_value = 0
    print("input pin [%] -> " % pin)
    return sensor_model.SensorReading(input_value)
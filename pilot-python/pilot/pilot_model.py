from enum import Enum
from itertools import repeat


class Constants:
    unknown = -1
    zero = 0


class FlightMode(Enum):

    grounded = 1
    taking_off = 2
    hovering = 3
    cruising = 4
    landing = 5


class FlightState:

    def __init__(self):
        self.distance_vector = list(repeat(Constants.unknown, 6))
        self.accln_vector = list(repeat(Constants.unknown, 6))
        self.mode = FlightMode.grounded

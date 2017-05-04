from abc import ABCMeta, abstractmethod
from enum import Enum
from raspi.fc.communication import FlightControlState
from raspi.fc.communication import FlightControlDelta


class AbstractFlightState(metaclass=ABCMeta):

    """
    A flight state is expressed as a combination of
    (a) Initial flight controller setting (A, E, T, R)
    (b) Flight control delta to be applied in each epoch
    (c) Optional exit condition
    """
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def initial_control_state(self):
        pass

    def control_state_delta(self):
        pass


class FlightSequence:

    def __init__(self, flight_stages):
        self.flight_stages = flight_stages


class FlightStage:

    def __init__(self, flight_state, duration, exit_condition):
        self.flight_state = flight_state
        self.duration = duration
        self.exit_condition = exit_condition


class FlightState(Enum):

    grounded = 1
    climb = 2
    hover = 3
    forward_cruise = 4
    backward_cruise = 5
    rotate = 6
    descent = 7
    steer_left = 8
    steer_right = 9


class HoverFlightState(AbstractFlightState):

    def __init__(self):
        super(self, HoverFlightState).__init__("hover")
        pass

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 2000)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, 0)


class ClimbFlightState(AbstractFlightState):

    def __init__(self, rate = 100):
        super(self, HoverFlightState).__init__("climb")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 2000)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, self.rate)


class DescendFlightState(AbstractFlightState):

    def __init__(self, rate = 100):
        super(self, HoverFlightState).__init__("descent")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 2000)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, -self.rate)


class CruiseForwardFlightState(AbstractFlightState):

    def __init__(self, rate = 100):
        super(self, HoverFlightState).__init__("cruise_forward")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 2000)

    def control_state_delta(self):
        return FlightControlDelta(0, -self.rate, 0, 0)


class CruiseBackwardFlightState(AbstractFlightState):

    def __init__(self, rate = 100):
        super(self, HoverFlightState).__init__("cruise_backward")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 2000)

    def control_state_delta(self):
        return FlightControlDelta(0, self.rate, 0, 0)


class GroundedFlightState(AbstractFlightState):

    def __init__(self):
        super(self, HoverFlightState).__init__("grounded")

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 0)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, 0)
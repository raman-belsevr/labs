from abc import ABCMeta, abstractmethod
from enum import Enum
from raspi.fc.communication import FlightControlState
from raspi.fc.communication import FlightControlDelta
from logging import Logging


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


class FlightSequenceIterator:

    """
    Iterator over a flight sequence that provides control values (A, E, R, T)
    for a complete flight sequence, transparently hopping over individual
    stage boundaries
    """
    def __init__(self, flight_sequence, drone_control_system):
        self.flight_sequence = flight_sequence
        self.stage_iterators = self.build_stage_iterators()
        self.stage_index = 0
        self.current_iterator = self.stage_iterators[self.stage_index]
        self.current_stage = self.flight_sequence.flight_stages[self.stage_index]
        self.drone_control_system = drone_control_system
        self.n_stages = flight_sequence.flight_stages.count
        self.next_epoch = 1

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if self.stage_index == 0 and self.next_epoch == 1:
                value = self.current_iterator.begin_state_delta(self)
            else:
                value = self.current_iterator.__next__()
        except StopIteration:
            Logging.logger.info("")
            self.stage_index += 1
            if self.stage_index == self.n_stages:
                raise StopIteration
            else:
                self.current_iterator = self.stage_iterators[self.stage_index]
                value = self.current_iterator.begin_state_delta()
        return value

    def build_stage_iterators(self):
        stage_iterators = [ FlightStageIterator(stage) for stage in self.flight_sequence.flight_stages]
        return stage_iterators


class FlightStage:

    def __init__(self, flight_state, duration, exit_condition):
        self.flight_state = flight_state
        self.duration = duration
        self.exit_condition = exit_condition


class FlightStageIterator:
    """
    Iterator over a flight stage that provides the control values (A, E, R, T)
    to execute a stage in steps (epochs) with each step executing in 0.02 seconds.
    """

    def __init__(self, flight_stage):
        self.next_epoch = 1
        self.max_epochs = flight_stage.duration/0.02
        self.flight_stage = flight_stage
        self.current = self.flight_stage.flight_state

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_epoch > self.max_epochs:
            raise StopIteration
        else:
            self.next_epoch += 1
            return self.current.flight_state.control_stage_delta

    def begin_state_delta(self, existing_state):
        desired_initial_state = self.flight_stage.flight_state.initial_control_state
        delta_aileron = desired_initial_state.aileron - existing_state.aileron
        delta_elevator = desired_initial_state.elevator - existing_state.elevator
        delta_rudder = desired_initial_state.rudder - existing_state.rudder
        delta_thrust = desired_initial_state.thrust - existing_state.thrust
        return FlightControlDelta(delta_aileron, delta_elevator, delta_rudder, delta_thrust)


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
        self.delta = FlightControlDelta(0, 0, 0, 0)

    def initial_control_state(self):
        return FlightControlState(1500, 1500, 1500, 2000)

    def control_state_delta(self):
        return self.delta


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
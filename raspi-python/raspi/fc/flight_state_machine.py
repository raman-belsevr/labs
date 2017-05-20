from abc import ABCMeta, abstractmethod
from enum import Enum
from raspi.fc.communication import FlightControlState
from raspi.fc.communication import FlightControlDelta
from raspi.raspi_logging import get_logger


class AbstractFlightState(metaclass=ABCMeta):

    logger = get_logger(__name__)

    """
    A flight state is expressed as a combination of
    (a) Initial flight controller setting (A, E, T, R)
    (b) Flight control delta to be applied in each epoch
    (c) Optional exit condition
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @abstractmethod
    def initial_control_state(self):
        pass

    def control_state_delta(self):
        pass


class FlightSequence:

    def __init__(self, flight_stages):
        self.flight_stages = flight_stages

    def __str__(self):
        return '\n'.join([str(stage) for stage in self.flight_stages])


class FlightSequenceSteps:

    logger = get_logger(__name__)

    def __init__(self, flight_sequence, flight_controller):
        self.flight_controller = flight_controller
        self.epoch = 0

        if flight_sequence is None:
            self.flight_sequence = None
            self.max_epoch = 0
            self.current_stage = None
            self.stage_steppers = None
        else:
            self.flight_sequence = flight_sequence
            self.max_epoch = len(self.flight_sequence.flight_stages)
            self.stage_steppers = self.build_stage_steps()
            self.current_stage = self.stage_steppers[self.epoch]

    def build_stage_steps(self):
        if self.flight_sequence is None:
            stage_steppers = list({})
        else:
            stage_steppers = [FlightStageSteps(stage, self.flight_controller) for stage in self.flight_sequence.flight_stages]
        return stage_steppers

    def next(self):
        if self.epoch == self.max_epoch:
            return None
        else:
            value = self.current_stage.next()
            if value is None:
                self.logger.info("Done with stage ([{}] of [{}])".format(self.epoch+1, self.max_epoch))
                self.epoch += 1
                if self.epoch == self.max_epoch:
                    return None
                else:
                    self.current_stage = self.stage_steppers[self.epoch]
                    return self.current_stage.next()
            else:
                return value


class FlightStage:

    def __init__(self, flight_state, duration, exit_condition=None):
        self.flight_state = flight_state
        self.duration = duration
        self.exit_condition = exit_condition

    def __str__(self):
        return "state[{}] duration[{}] exit_on[{}]".format(self.flight_state, self.duration, self.exit_condition)


class FlightStageSteps:
    """
    Iterator over a flight stage that provides the control values (A, E, R, T)
    to execute a stage in steps (epochs) with each step executing in 0.02 seconds.
    """

    logger = get_logger(__name__)

    def __init__(self, flight_stage, flight_controller):
        self.flight_stage = flight_stage
        self.flight_controller = flight_controller
        self.epoch = 0
        self.max_epoch = flight_stage.duration/0.02
        self.logger.info("Stage [{}] Max Epochs [{}]".format(self.flight_stage.flight_state.name, self.max_epoch))

    def next(self):
        if self.epoch == self.max_epoch:
            return None
        elif self.epoch == 0:
            self.epoch += 1
            return self.begin_state_delta(self.flight_controller.control_state)
        else:
            self.epoch += 1
            return self.flight_stage.flight_state.control_state_delta()

    def begin_state_delta(self, existing_state):
        desired_initial_state = self.flight_stage.flight_state.initial_control_state()
        self.logger.info("Begin stage [{}], transit from [{}] to [{}]".format(self.flight_stage.flight_state.name, existing_state, desired_initial_state))
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
        super().__init__("hover")
        self.delta = FlightControlDelta(0, 0, 0, 0)

    def initial_control_state(self):
        return FlightControlState(FlightControlState.AILERON_ZERO,
                                  FlightControlState.ELEVATOR_ZERO,
                                  FlightControlState.RUDDER_ZERO,
                                  FlightControlState.THROTTLE_MID)

    def control_state_delta(self):
        return self.delta


class ClimbFlightState(AbstractFlightState):

    def __init__(self, rate = 5):
        super(ClimbFlightState, self).__init__("climb")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(FlightControlState.AILERON_ZERO,
                                  FlightControlState.ELEVATOR_ZERO,
                                  FlightControlState.RUDDER_ZERO,
                                  FlightControlState.THROTTLE_MID)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, self.rate)


class DescendFlightState(AbstractFlightState):

    def __init__(self, rate = 5):
        super(DescendFlightState, self).__init__("descent")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(FlightControlState.AILERON_ZERO,
                                  FlightControlState.ELEVATOR_ZERO,
                                  FlightControlState.RUDDER_ZERO,
                                  FlightControlState.THROTTLE_MID)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, -self.rate)


class CruiseForwardFlightState(AbstractFlightState):

    def __init__(self, rate = 0):
        super(CruiseForwardFlightState, self).__init__("cruise_forward")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(FlightControlState.AILERON_ZERO,
                                  FlightControlState.ELEVATOR_FORWARD_MID,
                                  FlightControlState.RUDDER_ZERO,
                                  FlightControlState.THROTTLE_MID)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, 0)


class CruiseBackwardFlightState(AbstractFlightState):

    def __init__(self, rate = 0):
        super(CruiseBackwardFlightState, self).__init__("cruise_backward")
        self.rate = rate

    def initial_control_state(self):
        return FlightControlState(FlightControlState.AILERON_ZERO,
                                  FlightControlState.ELEVATOR_BACKWARD_MID,
                                  FlightControlState.RUDDER_ZERO,
                                  FlightControlState.THROTTLE_MID)

    def control_state_delta(self):
        return FlightControlDelta(0, self.rate, 0, 0)


class GroundedFlightState(AbstractFlightState):

    def __init__(self):
        super(GroundedFlightState, self).__init__("grounded")

    def initial_control_state(self):
        return FlightControlState(FlightControlState.AILERON_ZERO,
                                  FlightControlState.ELEVATOR_ZERO,
                                  FlightControlState.RUDDER_ZERO,
                                  FlightControlState.THROTTLE_ZERO)

    def control_state_delta(self):
        return FlightControlDelta(0, 0, 0, 0)
from abc import ABCMeta, abstractmethod
from enum import Enum
from raspi.raspi_logging import get_logger


class AbstractCommunicationProtocol(metaclass=ABCMeta):

    def __init__(self, proto_name):
        self.proto_name = proto_name

    @abstractmethod
    def send_rc_data(self, flight_control_state):
        """
        Send data signal directly to on-board RC receiver
        :param flight_control_input: FlightControlState
        """
        pass


class FlightControl(Enum):

    aileron = 1
    elevator = 2
    rudder = 3
    thrust = 4


class FlightControlState:

    logger = get_logger(__name__)

    def __init__(self, aileron, elevator, rudder, thrust):
        self.aileron = aileron
        self.elevator = elevator
        self.rudder = rudder
        self.thrust = thrust

    def to_list(self):
        return list({self.aileron, self.elevator, self.rudder, self.thrust})

    def change_aileron(self, delta):
        self.aileron += delta

    def change_elevator(self, delta):
        self.elevator += delta

    def change_rudder(self, delta):
        self.rudder += delta

    def change_thrust(self, delta):
        self.thrust += delta

    def apply(self, control_state_delta):
        self.logger.info("Applying control state delta [{}] to [{}]", control_state_delta, self)
        self.aileron = self.range_check(self.aileron, control_state_delta.delta_aileron, 0, 2000)
        self.elevator = self.range_check(self.elevator, control_state_delta.delta_elevator, 0, 2000)
        self.rudder = self.range_check(self.rudder, control_state_delta.delta_rudder, 0, 2000)
        self.thrust = self.range_check(self.thrust, control_state_delta.delta_thrust, 0, 2000)

    def __str__(self):
        return "Flight Control State A [{}] E[{}] R[{}] T[{}]".format(self.aileron,
                                                                      self.elevator,
                                                                      self.rudder,
                                                                      self.thrust)

    @staticmethod
    def range_check(value, delta, min, max):
        if value + delta > max:
            value = max
        elif value + delta < min:
            value = min
        else:
            value = value + delta
        return value




class FlightControlDelta:

    def __init__(self, delta_aileron, delta_elevator, delta_rudder, delta_thrust):
        self.delta_aileron = delta_aileron
        self.delta_elevator = delta_elevator
        self.delta_rudder = delta_rudder
        self.delta_thrust = delta_thrust

    def to_list(self):
        return list({self.delta_aileron, self.delta_elevator, self.delta_rudder, self.delta_thrust})

    def apply_to(self, existing_control_state):
        existing_control_state.apply(self)

    def __str__(self):
        return "FlightControlDelta: A [{}], E [{}], R [{}], T[{}]".format(self.delta_aileron,
                                                                          self.delta_elevator,
                                                                          self.delta_rudder,
                                                                          self.delta_thrust)
from abc import ABCMeta, abstractmethod
from enum import Enum


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

    def __init__(self, aileron, elevator, rudder, thrust):
        self.aileron = aileron
        self.elevator = elevator
        self.rudder = rudder
        self.thrust = thrust

    def to_list(self):
        return list(self.aileron, self.elevator, self.rudder, self.thrust)

    def change_aileron(self, delta):
        self.aileron += delta

    def change_elevator(self, delta):
        self.elevator += delta

    def change_rudder(self, delta):
        self.rudder += delta

    def change_thrust(self, delta):
        self.thrust += delta

    def apply(self, control_state_delta):
        self.aileron += control_state_delta.delta_aileron
        self.elevator += control_state_delta.delta_elevator
        self.rudder += control_state_delta.delta_rudder
        self.thrust += control_state_delta.delta_thrust


class FlightControlDelta:

    def __init(self, delta_aileron, delta_elevator, delta_rudder, delta_thrust):
        self.delta_aileron = delta_aileron
        self.delta_elevator = delta_elevator
        self.delta_rudder = delta_rudder
        self.delta_thrust = delta_thrust

    def to_list(self):
        return list(self.delta_aileron, self.delta_elevator, self.delta_rudder, self.delta_thrust)

    def apply_to(self, existing_control_state):
        existing_control_state.apply(self)

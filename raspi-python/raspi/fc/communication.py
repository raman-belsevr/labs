from abc import ABCMeta, abstractmethod
from enum import Enum
from raspi.raspi_logging import get_logger
from raspi.fc.util import SimpleEncoder
import json


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

    aileron  = 1
    elevator = 2
    rudder   = 3
    thrust   = 4


class FlightControlState:

    MULTI_DIR_CONTROL_MIN = -100
    MULTI_DIR_CONTROL_MAX = 100

    UNI_DIR_CONTROL_MIN = 0
    UNI_DIR_CONTROL_MAX = 100

    AILERON_MIN = -100
    AILERON_MAX = 100
    AILERON_ZERO = (AILERON_MIN + AILERON_MAX)/2

    ELEVATOR_MIN = -100
    ELEVATOR_MAX = 100
    ELEVATOR_ZERO = (ELEVATOR_MIN + ELEVATOR_MAX) / 2  # 0
    ELEVATOR_FORWARD_MID = ELEVATOR_MAX / 2
    ELEVATOR_BACKWARD_MID = ELEVATOR_MIN / 2

    RUDDER_MIN = -100
    RUDDER_MAX = 100
    RUDDER_RIGHT_MID = RUDDER_MAX / 2
    RUDDER_LEFT_MID = RUDDER_MIN / 2
    RUDDER_ZERO = (RUDDER_MIN + RUDDER_MAX)/2

    THROTTLE_MIN = 0
    THROTTLE_MAX = 100
    THROTTLE_MID = (THROTTLE_MAX + THROTTLE_MIN) / 2
    THROTTLE_DELTA = 1

    logger = get_logger(__name__)
    json_encoder = SimpleEncoder()

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
        self.logger.info("Applying control state delta [{}] to [{}]".format(control_state_delta, self))
        self.aileron = self.range_check(self.aileron, control_state_delta.delta_aileron, -100, 100)
        self.elevator = self.range_check(self.elevator, control_state_delta.delta_elevator, -100, 100)
        self.rudder = self.range_check(self.rudder, control_state_delta.delta_rudder, -100, 100)
        self.thrust = self.range_check(self.thrust, control_state_delta.delta_thrust, 0, 100)

    def __str__(self):
        return "Flight Control State A [{}] E[{}] R[{}] T[{}]".format(self.aileron,
                                                                      self.elevator,
                                                                      self.rudder,
                                                                      self.thrust)

    @staticmethod
    def range_check(value, delta, min, max):
        desired = value + delta
        if desired > max:
            value = max
        elif desired < min:
            value = min
        else:
            value = desired
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


class FlightLog:
    """
    Captures the flight control state (A, E, R, T) values at each time instant as received
    by a Flight Controller
    """

    buffer_limit = 100
    log_file_extension = "fclog"
    log_file_dir = "logs"
    logger = get_logger(__name__)

    def __init__(self, output_file):
        self.log = []
        self.output_file = self.log_file_dir + "/" + output_file + "." + self.log_file_extension
        self.file_handle = open(self.output_file, 'a')
        self.logger.info("Flight log at [{}]".format(self.output_file))

    def append(self, flight_control_data):
        if flight_control_data is not None:
            json_str = json.dumps(flight_control_data.__dict__)
            self.logger.info("json string is [{}]".format(json_str))
            self.log.append(json_str + '\n')
            if len(self.log) > self.buffer_limit:
                for line in self.log:
                    self.file_handle.write(line)
                self.log.clear()

    def flush(self):
        if len(self.log) > 0:
            self.file_handle.writelines(self.log)
            self.file_handle.flush()
            self.log.clear()

    def close(self):
        self.close()

    def __str__(self):
        return "Flight Log at [{}]".format(self.output_file)
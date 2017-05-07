from enum import Enum
from itertools import repeat
from raspi.raspi_logging import get_logger
from drone.drone_system import DroneSystem


class Pilot:
    logger = get_logger(__name__)

    def __init__(self):
        Pilot.logger.info("initializing pilot...")
        self.drone = DroneSystem("my_drone")
        self.atc = None
        self.flight_state = FlightState()
        Pilot.logger.info("initialized pilot")

    @staticmethod
    def validate_state(state):
        return state.any_errors == "false"

    def status(self):
        return self.drone.get_status()

    def execute_flight_sequence(self, flight_sequence):
        self.logger.info("executing flight sequence %s", flight_sequence)

    def fly(self, data):
        # provide 100 as delta thrust
        self.drone.control_system.change_thrust(100)

    def climb(self):
        self.drone.control_system.change_thrust(100)

    def descent(self, delta):
        self.drone.control_system.change_thrust(-100)

    def cruise(self, speed):
        # form a mix of commands to control system
        pass

    def steer_left(self, delta):
        self.drone.control_system.change_aileron(-delta)
        # form a mix of commands to control system
        pass

    def steer_right(self, delta):
        # form a mix of commands to control system
        self.drone.control_system.change_aileron(delta)
        pass

    def hover(self):
        # form a mix of commands to control system
        self.drone.control_system.set_flight_control(1500, 1500, 1500, 1500)
        pass

    def land(self, data):
        # form a mix of commands to control system
        pass

    def take_image(self):
        self.drone.media_system.image_front_left()

    def start(self):
        self.scheduler.schedule(self.fly)

    def end(self, data):
        self.scheduler.cancel(self.fly)


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

from pilot import Scheduler
from logging import Logging
from drone.drone_system import DroneSystem
from pilot.Model import FlightState


class Pilot:

    def __init__(self):
        Logging.logger.info("initializing pilot")
        self.drone = DroneSystem("my_drone")
        self.atc = None
        self.scheduler = Scheduler()
        self.flight_state = FlightState()

    @staticmethod
    def validate_state(state):
        return state.any_errors == "false"

    def status(self):
        return self.drone.get_status()

    def fly(self, data):
        # provide 100 as delta thrust
        self.drone.control_system.thrust(100)

    def climb(self, delta):
        self.drone.control_system.thrust(delta)

    def descent(self, delta):
        self.drone.control_system.thrust(delta)

    def cruise(self, speed):
        # form a mix of commands to control system
        pass

    def steer_left(self, delta):
        # form a mix of commands to control system
        pass

    def steer_right(self, delta):
        # form a mix of commands to control system
        pass

    def hover(self):
        # form a mix of commands to control system
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

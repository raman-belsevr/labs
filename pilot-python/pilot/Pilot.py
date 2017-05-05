from drone.drone_system import DroneSystem
from logging import Logging
from pilot import Scheduler
from pilot.Model import FlightState
from raspi.fc.flight_sequences import climb_hover_descent_grounded


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

    def execute_flight_sequence(self):
        sequence = climb_hover_descent_grounded()

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

from drone import Model
from pilot import FlightController
from pilot import Scheduler
from pilot import Model


class Pilot:

    def __init__(self):
        self.drone = Model.DroneSystem()
        self.flight_controller = FlightController(self.drone)
        self.atc = None
        self.scheduler = Scheduler()
        self.flight_state = Model.FlightState()

    @staticmethod
    def validate_state(state):
        return state.any_errors == "false"

    def desired_next_state(self, current_state):
        return current_state  # TODO fix this

    def fly(self):
        current_state = self.flight_controller.get_state()
        all_ok = Pilot.validate_state(current_state)
        if all_ok:
            desired = self.desired_next_state(current_state)
            self.flight_controller(current_state, desired)
        else:
            pass

    def start(self):
        self.scheduler.schedule(self.fly)

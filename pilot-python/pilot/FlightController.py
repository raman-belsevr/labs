from logging import Logging


class FlightController:

    def __init__(self, drone_system):
        self.drone = drone_system
        Logging.logger.info("Initialized flight controller")

    def get_state(self):
        return self.drone.get_state()

    def act(self, current_state, next_state):
        pass
from drone import Model


class FlightController:

    def __init__(self, drone_system):
        self.drone = drone_system

    def get_state(self):
        return self.drone.get_status()

    def act(self, current_state, next_state):
        pass
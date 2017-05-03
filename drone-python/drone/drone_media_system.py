from drone.drone_model import AbstractDroneMediaSystem


class DroneMediaSystem(AbstractDroneMediaSystem):

    def record_front_right(self):
        super().record_front_right()

    def image_front_left(self):
        super().image_front_left()

    def image_front_right(self):
        super().image_front_right()

    def record_front_left(self):
        super().record_front_left()

    def __init__(self):
        pass
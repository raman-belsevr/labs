from drone.drone_model import AbstractDroneMediaSystem
from drone.drone_model import Directions
from drone.drone_model import Sensor
from drone.drone_model import DroneMediaSystemStatus
from raspi.sensor.camera_sensor import CameraSensor
from drone.util import Util


class DroneMediaSystem(AbstractDroneMediaSystem):

    def record_front_right(self):
        pass

    def image_front_left(self):
        pass

    def image_front_right(self):
        pass

    def record_front_left(self):
        pass

    def __init__(self, name):
        super(DroneMediaSystem, self).__init__(name)

        # initialize front camera
        self.front_left_camera = self.camera_sensor(Directions.front_left)
        self.front_right_camera = self.camera_sensor(Directions.front_right)

        self.sensor_switcher = {
            self.front_left_camera.sensor_id: self.front_left_camera,
            self.front_right_camera.sensor_id: self.front_right_camera
        }

    @staticmethod
    def camera_sensor(direction):
        return CameraSensor(Util.sensor_id(Sensor.camera, direction))

    def get_status(self):
        # all sensors ok?
        return DroneMediaSystemStatus()

    def image(self, direction):
        sensor_id = self.sensor_id(Sensor.camera, direction)
        return self.sensor_switcher.get(sensor_id).get_reading()

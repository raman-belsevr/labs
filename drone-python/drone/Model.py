from raspi.sensor import sensor_model
from raspi.sensor import distance_sensor
from raspi.sensor import camera_sensor
from raspi.sensor import acceleration_sensor


# actuate sensors
class DroneSystem:

    def __init__(self):

        # initialize distance sensors
        self.distance_sensor_front = DroneSystem.distance_sensor(Directions.front)
        self.distance_sensor_rear = DroneSystem.distance_sensor(Directions.rear)
        self.distance_sensor_left = DroneSystem.distance_sensor(Directions.left)
        self.distance_sensor_right = DroneSystem.distance_sensor(Directions.right)
        self.distance_sensor_up = DroneSystem.distance_sensor(Directions.up)
        self.distance_sensor_down = sensor_model.DistanceSensor(Directions.down)

        # initialize front camera
        self.front_left_camera = camera_sensor(Directions.front_left)
        self.front_right_camera = camera_sensor(Directions.front_right)

        # initialize acceleration sensor
        self.acceleration_sensor = acceleration_sensor.AccelerationSensor()

        self.sensor_switcher = {
            self.distance_sensor_front.sensor_id : self.distance_sensor_front,
            self.distance_sensor_rear.sensor_id: self.distance_sensor_rear,
            self.distance_sensor_left.sensor_id: self.distance_sensor_left,
            self.distance_sensor_right.sensor_id: self.distance_sensor_right,
            self.distance_sensor_up.sensor_id: self.distance_sensor_up,
            self.distance_sensor_down.sensor_id: self.distance_sensor_down,
        }

    @staticmethod
    def sensor_id(sensor, direction):
        sensor + "_" + direction

    @staticmethod
    def distance_sensor(direction):
        return distance_sensor.UltraSonicDistanceSensor(DroneSystem.sensor_id(Sensor.distance, direction))

    @staticmethod
    def camera_sensor(direction):
        return camera_sensor.CameraSensor(DroneSystem.sensor_id(Sensor.camera, direction))

    def distance(self, direction):
        sensor_id = DroneSystem.sensor_id(Sensor.distance, direction)
        return self.sensor_switcher.get(sensor_id).get_reading()

    def image(self, direction):
        sensor_id = DroneSystem.sensor_id(Sensor.camera, direction)
        return self.sensor_switcher.get(sensor_id).get_reading()

    def acceleration(self):
        return self.acceleration_sensor.get_reading()

    def get_status(self):
        # all sensors ok?
        return DroneStatus()


class Sensor:

    distance = "distance"
    acceleration = "accln"
    camera = "camera"


class Directions:

    front = "front"
    rear = "rear"
    left = "left"
    right = "right"
    up = "up"
    down = "down"
    front_left = "front_left"
    front_right = "front_right"


class DroneStatus:

    def __init__(self):
        self.battery = 100
        self.front_distance_sensor = "ok"
        self.rear_distance_sensor = "ok"
        self.any_errors = "false"


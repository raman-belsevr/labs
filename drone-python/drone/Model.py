from raspi.sensor import sensor_model
from raspi.sensor import distance_sensor
from raspi.sensor import camera_sensor
from raspi.sensor import acceleration_sensor
from raspi.sensor import battery_sensor


# actuate sensors
class DroneSystem:

    def __init__(self):

        # initialize battery sensor
        self.battery_sensor = battery_sensor.BatterySensor(DroneSystem.sensor_id(Sensor.battery, ""))

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

        # waypoint sensor
        self.waypoint_sensor = waypoint_sensor.WaypointSensor()

        self.distance_sensor_switcher = {
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

    def distance_vector(self, include = list()):
        if include.count > 0:
            qualified_include = map(lambda sensor_id: Sensor.distance + "_" + sensor_id , include)
            reqd_sensors = list(filter(lambda sensor_id: sensor_id in qualified_include, self.distance_sensor_switcher.keys))
        else:
            reqd_sensors = list(self.distance_sensor_switcher.keys)

        distances = dict(map(lambda sensor_id: {sensor_id: self.distance_sensor_switcher.get(sensor_id).get_reading()}, reqd_sensors))
        return DistanceVector.build(distances)

    def accln_vector(self):
        return AcclnVector.build(self.acceleration_sensor.get_reading())


    @staticmethod
    def camera_sensor(direction):
        return camera_sensor.CameraSensor(DroneSystem.sensor_id(Sensor.camera, direction))

    def distance(self, direction):
        sensor_id = DroneSystem.sensor_id(Sensor.distance, direction)
        return self.distance_sensor_switcher.get(sensor_id).get_reading()

    def image(self, direction):
        sensor_id = DroneSystem.sensor_id(Sensor.camera, direction)
        return self.distance_sensor_switcher.get(sensor_id).get_reading()

    def acceleration(self):
        return self.acceleration_sensor.get_reading()

    def get_status(self):
        # all sensors ok?
        return DroneStatus()
    
    def get_state(self):
        distance_vector = self.distance_vector(list())
        accln_vector = self.accln_vector()



class Sensor:

    distance = "distance"
    acceleration = "accln"
    camera = "camera"
    battery = "battery"


class Directions:

    front = "front"
    rear = "rear"
    left = "left"
    right = "right"
    up = "up"
    down = "down"
    front_left = "front_left"
    front_right = "front_right"
    all = "all"

class DistanceVector:
    
    def __init__(self,
                 distance_front,
                 distance_rear,
                 distance_left,
                 distance_right,
                 distance_up,
                 distance_down):
        self.distance_front = distance_front
        self.distance_rear = distance_rear
        self.distance_left = distance_left
        self.distance_right = distance_right
        self.distance_up = distance_up
        self.distance_down  = distance_down

    @staticmethod
    def build(distance_dict):
        return DistanceVector(0, 0, 0, 0, 0, 0)


class AcclnVector:

    def __init__(self,
                 accln_front,
                 accln_right,
                 accln_up):
        self.accln_front = accln_front
        self.accln_right = accln_right
        self.accln_up  = accln_up

     @staticmethod
    def build(accln_reading):
        return AcclnVector(0, 0, 0) #TODO fix this!


class WayPoint:

    def __init__(self,
                 latitude,
                 longitude,
                 altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class DroneState:

    def __init__(self, distance_vector, accln_vector, way_point):
        self.distance_vector = distance_vector
        self.accln_vector = accln_vector
        self.way_point = way_point


class DroneStatus:

    def __init__(self):
        self.battery = 100
        self.front_distance_sensor = "ok"
        self.rear_distance_sensor = "ok"
        self.any_errors = "false"


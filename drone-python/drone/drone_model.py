from abc import ABCMeta, abstractmethod


class AbstractDroneSystem(metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def control_system(self):
        pass

    @abstractmethod
    def media_system(self):
        pass


class AbstractDroneControlSystem(metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def aileron(self, delta):
        pass

    @abstractmethod
    def thrust(self, delta):
        pass

    @abstractmethod
    def yaw(self, delta):
        pass

    @abstractmethod
    def roll(self, delta):
        pass


class AbstractDroneMediaSystem(metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def image_front_left(self):
        pass

    @abstractmethod
    def image_front_right(self):
        pass

    @abstractmethod
    def record_front_left(self):
        pass

    @abstractmethod
    def record_front_right(self):
        pass


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

    def __init__(self, accln_front, accln_right, accln_up):
        self.accln_front = accln_front
        self.accln_right = accln_right
        self.accln_up = accln_up

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
    """
    Represents the dynamic instantaneous state of a drone
    """
    def __init__(self, distance_vector, accln_vector, way_point):
        self.distance_vector = distance_vector
        self.accln_vector = accln_vector
        self.way_point = way_point


class DroneStatus:
    """
    Represents the health of the drone, i.e. battery life remaining and
    working status of on-board sensors.
    """
    def __init__(self):
        self.battery = 100
        self.front_distance_sensor = "ok"
        self.rear_distance_sensor = "ok"
        self.any_errors = "false"


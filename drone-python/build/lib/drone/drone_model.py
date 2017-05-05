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
    def change_aileron(self, delta):
        pass

    @abstractmethod
    def change_thrust(self, delta):
        pass

    @abstractmethod
    def change_rudder(self, delta):
        pass

    @abstractmethod
    def change_elevator(self, delta):
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
    def __init__(self, control_status, media_status):
        self.control_status = control_status
        self.media_status = media_status
        self.all_ok = self.control_status.all_ok and self.media_status.all_ok


class DroneControlSystemStatus:
    """
    Represents the health of the drone's control system, i.e. battery life remaining and
    working status of on-board sensors.
    """

    def __init__(self, sensor_report, all_ok):
        self.sensor_report = sensor_report
        self.all_ok = all_ok


class DroneMediaSystemStatus:
    """
    Represents the health of the drone's media system, i.e. camera, microphone etc.
    """

    def __init__(self, sensor_report, all_ok):
        self.sensor_report = sensor_report
        self.all_ok = all_ok


class SensorReport:

    def __init__(self, sensors):
        self.report = dict()
        for sensor in sensors:
            self.report[sensor.sensor_id] = sensor.is_ok()

    def __str__(self):
        display_str = ''
        for key in self.report:
            display_str += key + ' -> ' + self.report[key]
        return display_str

    def get_not_working(self):
        return dict((key, value) for key, value in self.report.iteritems() if value.is_ok is False)


from drone.drone_model import AbstractDroneControlSystem
from drone.drone_model import AcclnVector
from drone.drone_model import Directions
from drone.drone_model import DistanceVector
from drone.drone_model import DroneState
from drone.drone_model import DroneControlSystemStatus
from drone.drone_model import Sensor
from raspi.fc.fc_model import FlightControlState
from raspi.fc.fc_model import FlightController
from raspi.fc.flight_state_machine import FlightSequenceIterator
from raspi.sensor.acceleration_sensor import AccelerationSensor
from raspi.sensor.battery_sensor import BatterySensor
from raspi.sensor.camera_sensor import CameraSensor
from raspi.sensor.distance_sensor import UltraSonicDistanceSensor
from raspi.sensor.waypoint_sensor import WaypointSensor
from drone.drone_model import SensorReport


class DroneControlSystem(AbstractDroneControlSystem):

    def load_flight_sequence(self, flight_sequence):
        self.flight_controller.load_flight_sequence(flight_sequence)

    def abort_flight_sequence(self):
        self.flight_controller.reset_flight_sequence

    def change_aileron(self, delta):
        self.flight_controller.change_aileron(delta)

    def change_elevator(self, delta):
        self.flight_controller.change_elevator(delta)

    def change_rudder(self, delta):
        self.flight_controller.change_rudder(delta)

    def change_thrust(self, delta):
        self.set_flight_control_delta()
        self.flight_controller.thrust(delta)

    def set_flight_control(self, aileron, elevator, rudder, thrust):
        self.flight_controller.set_flight_control_state(FlightControlState(aileron, elevator, rudder, thrust))

    def __init__(self, name):
        super(DroneControlSystem, self).__init__(name)

        # set empty flight sequence
        self.flight_sequence = None
        self.flight_sequence_iterator = FlightSequenceIterator(self.flight_sequence, self)

        # initialize flight controller
        self.flight_controller = FlightController("spf3", "usb_port")

        # initialize battery sensor
        self.battery_sensor = BatterySensor(self.sensor_id(Sensor.battery, ""))

        # initialize distance sensors
        self.distance_sensor_front = self.distance_sensor(direction=Directions.front)
        self.distance_sensor_rear = self.distance_sensor(Directions.rear)
        self.distance_sensor_left = self.distance_sensor(Directions.left)
        self.distance_sensor_right = self.distance_sensor(Directions.right)
        self.distance_sensor_up = self.distance_sensor(Directions.up)
        self.distance_sensor_down = self.distance_sensor(Directions.down)

        # initialize acceleration sensor
        self.acceleration_sensor = AccelerationSensor()

        # waypoint sensor
        self.waypoint_sensor = WaypointSensor()

        self.sensor_switcher = {
            self.distance_sensor_front.sensor_id: self.distance_sensor_front,
            self.distance_sensor_rear.sensor_id: self.distance_sensor_rear,
            self.distance_sensor_left.sensor_id: self.distance_sensor_left,
            self.distance_sensor_right.sensor_id: self.distance_sensor_right,
            self.distance_sensor_up.sensor_id: self.distance_sensor_up,
            self.distance_sensor_down.sensor_id: self.distance_sensor_down,
            self.waypoint_sensor.sensor_id: self.waypoint_sensor
        }

    @staticmethod
    def distance_sensor(self, direction):
        return UltraSonicDistanceSensor(self.sensor_id(self.Sensor.distance, direction))

    @staticmethod
    def camera_sensor(self, direction):
        return CameraSensor(self.sensor_id(self.Sensor.camera, direction))

    @staticmethod
    def sensor_id(sensor, direction):
        return sensor + "_" + direction

    def distance_vector(self, include=list()):
        if include.count > 0:
            qualified_include = map(lambda sensor_id: Sensor.distance + "_" + sensor_id, include)
            reqd_sensors = list(filter(lambda sensor_id: sensor_id in qualified_include, self.sensor_switcher.keys))
        else:
            reqd_sensors = list(self.sensor_switcher.keys)

        distances = dict(
            map(lambda sensor_id: {sensor_id: self.sensor_switcher.get(sensor_id).get_reading()}, reqd_sensors))
        return DistanceVector.build(distances)

    def accln_vector(self):
        return AcclnVector.build(self.acceleration_sensor.get_reading())

    def distance(self, direction):
        sensor_id = self.sensor_id(Sensor.distance, direction)
        return self.sensor_switcher.get(sensor_id).get_reading()

    def acceleration(self):
        return self.acceleration_sensor.get_reading()

    def get_status(self):
        # all sensors ok?
        sensor_report = SensorReport(self.sensor_switcher.values())
        all_ok = self.all_ok()
        return DroneControlSystemStatus(sensor_report, all_ok)

    def all_ok(self):
        for key, value in self.report.iteritems():
            if value.is_ok is False:
                return False
        return True

    def get_state(self):
        distance_vector = self.distance_vector(list())
        accln_vector = self.accln_vector()
        way_point = self.waypoint_sensor()
        return DroneState(distance_vector, accln_vector, way_point)

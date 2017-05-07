from drone import drone_model
from raspi.sensor import distance_sensor
from raspi.sensor import camera_sensor
from raspi.sensor.distance_sensor import UltraSonicDistanceSensor


@staticmethod
class Util:
    def sensor_id(sensor, direction):
        return sensor + "_" + direction

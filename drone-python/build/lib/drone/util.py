from drone import drone_model
from raspi.sensor import distance_sensor
from raspi.sensor import camera_sensor
from raspi.sensor.distance_sensor import UltraSonicDistanceSensor


class Util:

    @staticmethod
    def sensor_id(sensor, direction):
        sensor + "_" + direction



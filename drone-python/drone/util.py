from drone import drone_model
from raspi.sensor import distance_sensor


def sensor_id(sensor, direction):
    sensor + "_" + direction


def distance_sensor(direction):
    return distance_sensor.UltraSonicDistanceSensor(sensor_id(drone_model.Sensor.distance, direction))


def camera_sensor(direction):
    return camera_sensor.CameraSensor(sensor_id(drone_model.Sensor.camera, direction))
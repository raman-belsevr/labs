from raspi.sensor import sensor_model
from drone.drone_model import WayPoint


class WaypointSensor(sensor_model.AbstractSensor):

    """
    Latitude-Longitude-Altitude sensor
    """

    def is_ok(self):
        return "true"

    def __init__(self, sensor_id):
        self.sensor = LatLongAltSensor()
        super(WaypointSensor, self).__init__(sensor_id)

    def get_ic(self):
        return "lat_Long_alt_sensor"

    def get_reading(self):
        input_value = self.sensor.waypoint
        return sensor_model.SensorReading(input_value)


class LatLongAltSensor:

    def __init__(self):
        pass

    def waypoint(self):
        return WayPoint(0,0,0)






from raspi.sensor import sensor_model
#from mpu6050 import mpu6050


class AccelerationSensor(sensor_model.AbstractSensor):
    """
    https://pypi.python.org/pypi/mpu6050-raspberrypi/
    """

    def __init__(self, sensor_id):
        self.sensor = DummyAcclerationSensor() #mpu6050(0x68)
        super(AccelerationSensor, self).__init__(sensor_id)

    def get_ic(self):
        return "acceleration sensor"

    def get_reading(self):
        """
        Gets and returns the X, Y and Z values from the accelerometer.

        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.

        :return:
        """
        accelerometer_data = self.sensor.get_accel_data(g=False)
        return sensor_model.SensorReading(accelerometer_data)

    def is_ok(self):
        return "true"


class DummyAcclerationSensor:

    def __init__(self):
        pass

    def get_accel_data(self, g):
        return 0
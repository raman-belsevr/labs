from raspi.sensor import sensor_model


class BatterySensor(sensor_model.AbstractSensor):

    """
    Provides reading of the on-board battery
    """

    def get_reading(self):
        self.batter_sensor.get_voltage()

    def is_ok(self):
        return True

    def get_ic(self):
        return "lipo_battery"

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.batter_sensor = BatteryIC()
        super(BatterySensor, self).__init__(sensor_id)


class BatteryIC:

    def __init__(self):
        pass

    def get_voltage(self):
        return 5
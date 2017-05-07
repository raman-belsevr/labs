from raspi.sensor import sensor_model
#from gpiozero import DistanceSensor


class UltraSonicDistanceSensor(sensor_model.AbstractSensor):

    """
    Ultrosound-based distance sensor
    """

    def is_ok(self):
        return "true"

    def __init__(self, sensor_id, echo=17, trigger=4, threshold_distance=0.5, max_distance=2):
        self.ultrasonic = DummyDistanceSensor(0)
        #DistanceSensor(echo, trigger, threshold_distance, max_distance)
        #DistanceSensor.__configure__()
        super(UltraSonicDistanceSensor, self).__init__(sensor_id)

    def get_ic(self):
        return "ultra_sonic_distance_sensor"

    def get_reading(self):
        input_value = self.ultrasonic.distance
        return sensor_model.SensorReading(input_value)

    def wait_for_in_range(self):
        """
        Blocking call that waits until the sensor detects distance in range
        :return:
        """
        self.ultrasonic.wait_for_in_range()
        print("In range")

    def wait_for_out_of_range(self):
        """
        Blocking call that waits until the sensor detects being out of range
        :return:
        """
        self.ultrasonic.wait_for_out_of_range()
        print("Out of range")

    def when_in_range(self, f):
        """
        Asynchronous call with a configure callback that is invoked when the sensor
        detects being in range
        :param f: callback
        """
        self.ultrasonic.when_in_range = f

    def when_out_of_range(self, f):
        """Asynchronous call with a configure callback that is invoked when the sensor
           detects being out of range
           :param f: callback
        """
        self.ultrasonic.when_out_of_range = f


class DummyDistanceSensor:

    def __init__(self, distance):
        self.distance = distance





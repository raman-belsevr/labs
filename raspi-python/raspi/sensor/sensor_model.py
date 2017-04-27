from abc import ABCMeta, abstractmethod
import datetime
import uuid


class AbstractSensor (metaclass=ABCMeta):
    """
    Example class:
    Provides an abstraction over the interface of an actual IC.
    """

    def __init__(self):
        self.sensor_id = uuid.uuid4

    @abstractmethod
    def get_ic(self):
        """:return: the IC identifier for the sensor"""
        pass

    @abstractmethod
    def get_reading(self):
        """
        :return: reading obtained from the sensor
        """
        pass

    @abstractmethod
    def is_ok(self):
        pass


class SensorReading:
    """
    Wrapper class that augments a reading obtained from a sensor
    with the a timestamp
    """
    def __init__(self, value):
        self.reading = value
        self.ts = datetime.datetime.now()





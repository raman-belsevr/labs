from abc import ABCMeta, abstractmethod
from enum import Enum


class AbstractCommunicationProtocol(metaclass=ABCMeta):

    def __init__(self, proto_name):
        self.proto_name = proto_name

    @abstractmethod
    def send_rc_data(self, data):
        """
        Send data signal directly to on-board RC receiver
        :param data:
        """
        pass


class FlightControl(Enum):

    aileron = 1
    thrust = 2
    yaw = 3
    roll = 4

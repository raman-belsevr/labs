from drone.drone_model import AbstractDroneSystem
from drone.drone_control_system import DroneControlSystem
from drone.drone_media_system import DroneMediaSystem
from logging.Logging import get_logger


class DroneSystem(AbstractDroneSystem):

    logger = get_logger(__name__)

    def control_system(self):
        return self.control_system

    def media_system(self):
        return self.media_system

    def __init__(self, name):
        self.control_system = DroneControlSystem(name)
        self.media_system = DroneMediaSystem(name)
        DroneSystem.logger.info("initialized drone %s", name)
from sim.control.generic_controller import GenericController
from enum import Enum
import json

class LogReplayController(GenericController):
    """
    Replay flight controls from a log file
    """

    def __init__(self, log_file):
        super().__init__("log_file_replay")
        self.log_file = open(log_file, "r")
        self.current_chunk = []
        self.current_log = None
        self.current_log_index = 0

    def _get_pitch(self):
        return self._read_control_input(ControlInput.elevator.name)

    def _get_roll(self):
        return self._read_control_input(ControlInput.aileron.name)

    def _get_yaw(self):
        return self._read_control_input(ControlInput.rudder.name)

    def _get_throttle(self):
        return self._read_control_input(ControlInput.throttle.name)

    def _get_switchval(self):
        return 0

    def _mark_done(self):
        self.current_log_index += 1
        self.current_log = None

    def _read_control_input(self, control_input):
        # chunk has not been loaded or has been completely processed
        if self.current_log is None:
            if self.current_log_index == len(self.current_chunk):
                self.current_chunk = self.next_chunk(self.log_file)
                if len(self.current_chunk) == 0:
                    self.log_file.close()
                    return super().END_OF_INPUT
                self.current_log_index = 0
            current_input = self.current_chunk[self.current_log_index]
            self.current_log = json.loads(current_input)

        return self.current_log[control_input]

    @staticmethod
    def next_chunk(file_obj, chunk_size=2048):
        """
        Lazy function to read a file piece by piece.
        Default chunk size: 2kB.
        """
        while True:
            data = file_obj.read(chunk_size)
            if not data:
                break
            yield data

class ControlInput(Enum):
    aileron = 0
    elevator = 1
    rudder = 2
    throttle = 3
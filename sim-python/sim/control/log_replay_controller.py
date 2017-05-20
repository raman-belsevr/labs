from sim.control.generic_controller import GenericController
from enum import Enum
import json


class LogReplayController(GenericController):
    """
    Replay flight controls from a log file
    """

    def __init__(self, switch_labels, log_file="./controller.log"):
        super().__init__("log_file_replay", switch_labels)

        self.log_file = open(log_file, "r")
        self.current_log = None
        self.current_log_index = 0
        self.logs = self.log_file.readlines()

    def _get_pitch(self):
        return self._read_control_input(ControlInput.elevator.name)

    def _get_roll(self):
        return self._read_control_input(ControlInput.aileron.name)

    def _get_yaw(self):
        return self._read_control_input(ControlInput.rudder.name)

    def _get_throttle(self):
        return self._read_control_input(ControlInput.thrust.name)

    def _get_switchval(self):
        return 0

    def _mark_done(self):
        self.current_log = None

    def _read_control_input(self, control_input):
        # chunk has not been loaded or has been completely processed
        if self.current_log is None:
            if self.current_log_index == len(self.logs):
                return 0
            else:
                self.current_log = json.loads(self.logs[self.current_log_index])
                print("[{}] -> Line: [{}]".format(self.current_log_index, self.current_log))
                self.current_log_index += 1
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

    @staticmethod
    def next_line(file_ob):
        for line in file_ob:
            yield line


class ControlInput(Enum):
    aileron = 0
    elevator = 1
    rudder = 2
    thrust = 3


if __name__ == "__main__":
    reply_controller = LogReplayController(None, "/Users/ramang/research/work/belsevr/labs/logs/20170512-121540.fclog")
    while True:
        reply_controller._read_control_input("aileron")
        reply_controller._read_control_input("elevator")
        reply_controller._read_control_input("rudder")
        reply_controller._read_control_input("thrust")
        reply_controller._mark_done()
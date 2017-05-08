import threading
import time

import serial

from raspi import raspi_logging
from raspi.fc import multiwii_serial_protocol
from raspi.fc.communication import FlightControlDelta
from raspi.fc.communication import FlightControlState
from raspi.fc.flight_sequences import grounded_sequence
from raspi.fc.flight_sequences import hover_sequence
from raspi.fc.flight_state_machine import FlightSequenceSteps
from raspi.raspi_logging import get_logger


class FlightController:

    logger = get_logger(__name__)

    def __init__(self, name, port):

        ########################################
        # Initialization of controller options #
        ########################################

        self.name = name     # Name of the flight controller hardware chip
        self.started = True  # Indicating whether flight controller is operational or not
        self.reset_flight_sequence = False

        self.ATT = 0      # Ask the attitude of the multicopter
        self.ATT = 0      # Ask the altitude of the multicopter
        self.SET_RC = 1   # Set rc command
        self.PRINT = 0    # Print data to terminal
        self.timeMSP = 0.02 # sleeping interval in spin-loop

        ##################################
        # Communication with serial port #
        ##################################
        self.port = port
        self.ser = serial.Serial()
        self.configure_serial_port(self.ser)


        ###############################
        # Select Serial Protocol
        ##############################
        self.protocol = multiwii_serial_protocol.MultiwiiSerialProtocol()

        ###############################
        # Initialize Global Variables
        ###############################
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = -0
        self.heading = -0
        self.timestamp = -0
        self.gpsString = -0
        self.numSats = -0
        self.accuracy = -1
        self.beginFlag = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.throttle = 0
        self.angx = 0.0
        self.angy = 0.0
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0
        self.message = ""
        self.ax = 0
        selfay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0
        self.magx = 0
        self.magy = 0
        self.magz = 0
        self.elapsed = 0
        self.flytime = 0
        self.numOfValues = 0
        self.precision = 3
        self.control_state = FlightControlState(1500, 1500, 1500, 1500) # order -> roll(A), pitch(E), yaw(R), throttle(T)
        self.control_state_delta = FlightControlDelta(0, 0, 0, 0)

        #######################################
        # Initialize Grounded Flight Sequence #
        #######################################
        self.flight_sequence = None
        self.flight_sequence_stepper = FlightSequenceSteps(self.flight_sequence, self)

        self.loopThread = threading.Thread(target=self.loop)
        self.logger.info("Initialized flight controller %s", name)
        time.sleep(5)
        self.loopThread.start()

        if self.ser.isOpen():
            print("Wait 5 sec for calibrate the communication protocol")
            time.sleep(5)
            self.loopThread.start()

    def configure_serial_port(self, ser):
        ser.port = self.port
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 0
        ser.xonxoff = False
        ser.rtscts = False
        ser.dsrdtr = False
        ser.writeTimeout = 2

        """
        try:
            ser.open()
        except Exception as e:
            self.logger.error("Unable to open serial port %s" % str(e))
            #exit()
        """

    def stop(self):
        self.started = False

    def load_flight_sequence(self, new_sequence):
        self.flight_sequence = new_sequence
        self.reset_flight_sequence = True

    def abort_flight_sequence(self):
        self.flight_sequence = hover_sequence()
        self.reset_flight_sequence = True

    def change_aileron(self, delta):
        self.control_state_delta.delta_aileron = delta

    def change_elevator(self, delta):
        self.control_state_delta.delta_elevator = delta

    def change_rudder(self, delta):
        self.control_state_delta.delta_rudder = delta

    def change_thrust(self, delta):
        self.control_state_delta.delta_thrust = delta

    def set_flight_control_state(self, control_state):
        self.control_state = control_state

    def set_flight_control_state(self, aileron, elevator, rudder, thrust):
        self.control_state = FlightControlState(aileron, elevator, rudder, thrust)

    def set_flight_control_delta(self, control_state_delta):
        self.control_state_delta = control_state_delta

    def loop(self):
        try:

            while self.started:
                if self.SET_RC:
                    # apply flight control delta to existing state and
                    # send modified flight control state (A,E,T,R) to flight controller
                    if self.reset_flight_sequence is True:
                        # reload new flight sequence
                        self.logger.info("Reloading new flight sequence [{}]".format(self.flight_sequence))
                        self.flight_sequence_stepper = FlightSequenceSteps(self.flight_sequence, self)
                        self.reset_flight_sequence = False

                    self.control_state_delta = self.flight_sequence_stepper.next()
                    if self.control_state_delta is None:
                        self.logger.debug("Finished executing flight sequence [{}]".format(self.flight_sequence))
                    else:
                        self.control_state.apply(self.control_state_delta)
                        self.logger.debug("Applied delta [{}] to state [{}]".format(self.control_state_delta, self.control_state))
                        #self.protocol.send_rc_data(8, self.control_state)
                        time.sleep(self.timeMSP)
            self.logger.info("Closing connection with flight controller chip")
            #self.ser.close()
        except Exception as e:
            self.logger.error("Exception in operating flight controller loop %s", str(e))
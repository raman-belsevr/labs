import serial
import time
import threading
from raspi.fc import multiwii_serial_protocol
from logging import Logging


class FlightController:

    def __init__(self, name, port):

        ########################################
        # Initialization of controller options #
        ########################################

        self.name = name     # Name of the flight controller hardware chip
        self.started = True  # Indicating whether flight controller is operational or not

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
        self.rcData = [1500, 1500, 1500, 1500]  # order -> roll, pitch, yaw, throttle

        self.loopThread = threading.Thread(target=self.loop)
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

        try:
            ser.open()
        except Exception as e:
            Logging.logger.error("Unable to open serial port % " % str(e))
            exit()

    def stop(self):
        self.started = False

    def send_rc_data(self, rc_data):
        self.rcData = rc_data

    def loop(self):
        try:
            while self.started:
                if self.SET_RC:
                    self.protocol.send_rc_data(8, self.rcData)
                    time.sleep(self.timeMSP)
            self.ser.close()
        except Exception as e:
            Logging.logger.error("Exception in operating flight controller loop")
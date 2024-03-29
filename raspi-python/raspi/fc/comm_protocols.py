import struct		# for decoding data strings
from raspi.fc.communication import AbstractCommunicationProtocol
from raspi.raspi_logging import get_logger


class MultiwiiSerialProtocol(AbstractCommunicationProtocol):

    def send_rc_data(self, fcs):
        self.send_rc_data(8, self.adjust_flight_control_data(fcs)) #TODO fix this!

    @staticmethod
    def adjust_flight_control_data(fcs):
        # valid range = 0, 2000
        values = [1500 + (fcs.aileron/100)*500, 1500 + (fcs.elevator / 100) * 500, 1500 + (fcs.rudder / 100) * 500,
                  1500 + (fcs.throttle / 100) * 500]
        return values

    def send_rc_data(self, data_length, data):
        checksum = 0
        code = self.CMD2CODE["MSP_SET_RAW_RC"]
        total_data = ['$', 'M', '<', data_length, code] + data
        for i in struct.pack('<2B%dh' % len(data), *total_data[3:len(total_data)]):
            checksum = checksum ^ ord(i)

        total_data.append(checksum)

        try:
            b = None
            b = self.ser.write(struct.pack('<3c2B%dhB' % len(data), *total_data))
        except Exception as ex:
            print
            'send data error'
            print(ex)
        return b

    def __init__(self):
        ###############################
        # Multiwii Serial Protocol
        # Hex value for MSP request
        ##############################
        self.BASIC = "\x24\x4d\x3c\x00"  # MSG Send Header (to MultiWii)
        self.MSP_IDT = self.BASIC + "\x64\x64"  # MSG ID: 100
        self.MSP_STATUS = self.BASIC + "\x65\x65"  # MSG ID: 101
        self.MSP_RAW_IMU = self.BASIC + "\x66\x66"  # MSG ID: 102
        self.MSP_SERVO = self.BASIC + "\x67\x67"  # MSG ID: 103
        self.MSP_MOTOR = self.BASIC + "\x68\x68"  # MSG ID: 104
        self.MSP_RC = self.BASIC + "\x69\x69"  # MSG ID: 105
        self.MSP_RAW_GPS = self.BASIC + "\x6A\x6A"  # MSG ID: 106
        self.MSP_ATTITUDE = self.BASIC + "\x6C\x6C"  # MSG ID: 108
        self.MSP_ALTITUDE = self.BASIC + "\x6D\x6D"  # MSG ID: 109
        self.MSP_BAT = self.BASIC + "\x6E\x6E"  # MSG ID: 110
        self.MSP_COMP_GPS = self.BASIC + "\x71\x71"  # MSG ID: 111
        self.MSP_SET_RC = self.BASIC + "\xC8\xC8"  # MSG ID: 200

        self.CMD2CODE = {
            # Getter
            'MSP_IDENT': 100,
            'MSP_STATUS': 101,
            'MSP_RAW_IMU': 102,
            'MSP_SERVO': 103,
            'MSP_MOTOR': 104,
            'MSP_RC': 105,
            'MSP_RAW_GPS': 106,
            'MSP_COMP_GPS': 107,
            'MSP_ATTITUDE': 108,
            'MSP_ALTITUDE': 109,
            'MSP_ANALOG': 110,
            'MSP_RC_TUNING': 111,
            'MSP_PID': 112,
            'MSP_BOX': 113,
            'MSP_MISC': 114,
            'MSP_MOTOR_PINS': 115,
            'MSP_BOXNAMES': 116,
            'MSP_PIDNAMES': 117,
            'MSP_WP': 118,
            'MSP_BOXIDS': 119,

            # Setter
            'MSP_SET_RAW_RC': 200,
            'MSP_SET_RAW_GPS': 201,
            'MSP_SET_PID': 202,
            'MSP_SET_BOX': 203,
            'MSP_SET_RC_TUNING': 204,
            'MSP_ACC_CALIBRATION': 205,
            'MSP_MAG_CALIBRATION': 206,
            'MSP_SET_MISC': 207,
            'MSP_RESET_CONF': 208,
            'MSP_SET_WP': 209,
            'MSP_SWITCH_RC_SERIAL': 210,
            'MSP_IS_SERIAL': 211,
            'MSP_DEBUG': 254,
        }
        super().__init__("multiwii")


class LogOnlyProtocol(AbstractCommunicationProtocol):

    logger = get_logger(__name__)

    def __init__(self):
        super().__init__("log_only")

    def send_rc_data(self, fcs):
        self.logger.info("A [{}], E [{}], R [{}], T [{}]".format(fcs.aileron, fcs.elevator, fcs.rudder, fcs.thrust))

import struct
import time


class Util:

    # Timeout for receiving data from client
    TIMEOUT_SEC = 1.0
    MAX_MSG_LEN = 1000

    # Helper functions ================================================================
    @staticmethod
    def send_floats(client, data):
        client.send(struct.pack('%sf' % len(data), *data))

    @staticmethod
    def unpack_floats(msg, nfloats):
        return struct.unpack('f' * nfloats, msg)

    @staticmethod
    def receive_floats(client, nfloats):
        # We use 32-bit floats
        msgsize = 4 * nfloats

        # Implement timeout
        start_sec = time.time()
        remaining = msgsize
        msg_bytes = bytes()
        while remaining > 0:
            msg_bytes += client.recv(remaining)
            remaining -= len(msg_bytes)
            if (time.time() - start_sec) > Util.TIMEOUT_SEC:
                return None
        print("Bytes received [{}]".format(msg_bytes))
        return Util.unpack_floats(msg_bytes, nfloats)

    @staticmethod
    def receive_float(client):
        # We use 32-bit floats
        msgsize = 4

        # Implement timeout
        start_sec = time.time()
        remaining = msgsize
        while remaining > 0:
            msg_bytes = client.recv(remaining)
            print("message received (bytes) is [{}]".format(msg_bytes))
            value = struct.unpack('f', msg_bytes)
            remaining -= len(msg_bytes)
            if (time.time() - start_sec) > Util.TIMEOUT_SEC:
                return None
        return value

    @staticmethod
    def receive_string(client):
        expected_msg_len = int(Util.receive_float(client)[0])
        msg_bytes = client.recv(expected_msg_len)
        msg = msg_bytes.decode("utf-8")
        print("String received is [{}]".format(msg))
        return msg

    @staticmethod
    def scalar_to_3d(s, a):
        return [s * a[2], s * a[6], s * a[10]]

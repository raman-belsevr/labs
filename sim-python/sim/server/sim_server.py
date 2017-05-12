#!/usr/bin/env python

'''
sim_server.py - Automatically-launched Python server script for PyQuadSim

Translates simulation values from V-REP to sensor values for quadrotor model

    Copyright (C) 2014 Bipeen Acharya, Fred Gisa, and Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

'''

# Import your controller here =====================================================

from sim.control.log_replay_controller import LogReplayController as Controller
#from sim.control.keyboard import Keyboard as Controller

# Mission-specific data ===========================================================


# Simulation parameters ===========================================================



# Other imports ===================================================================

from sys import argv, exit
import struct
import time
import os

from sim.server.socket_server import serve_socket
from sim.physics.fmu import FMU
from sim.server.utils import Util



# Helper functions ================================================================

def send_floats(client, data):

    client.send(struct.pack('%sf' % len(data), *data))

def unpack_floats(msg, nfloats):
    return struct.unpack('f'*nfloats, msg)

def receive_floats(client, nfloats):
    # We use 32-bit floats
    msgsize = 4 * nfloats

    # Implement timeout
    start_sec = time.time()
    remaining = msgsize
    msg = ''
    while remaining > 0:
        msg += client.recv(remaining)
        remaining -= len(msg)
        if (time.time()-start_sec) > TIMEOUT_SEC:
            return None

    return unpack_floats(msg, nfloats)


def receive_string(client):
    return client.recv(int(receive_floats(client, 1)[0]))


def scalar_to_3d(s, a):
    return [s*a[2], s*a[6], s*a[10]]
    
# LogFile class ======================================================================================================

class LogFile(object):

    def __init__(self, directory):
 
        self.fd = open(directory + '/' + time.strftime('%d_%b_%Y_%H_%M_%S') + '.csv', 'w')

    def writeln(self, string):

        self.fd.write(string + '\n')
        self.fd.flush()

    def close(self):

        self.fd.close()

# Initialization =====================================================================================================

# Require controller
controller = Controller(('Stabilize', 'Hold Altitude', 'Unused'))

# Serve a socket on the port indicated in the first command-line argument
client = serve_socket(int(argv[1]))

# Receive working directory path from client
sim_directory = Util.receive_string(client)

# Create logs folder if needed
logdir = sim_directory + '/logs'

if not os.path.exists(logdir):
    os.mkdir(logdir)

# Open logfile named by current date, time
logfile = LogFile(logdir)

# Create an FMU object, passing it the logfile object in case it needs to write to the logfile.
fmu = FMU(logfile)

# Loop ==========================================================================================================

prevtime = time.time()


def get_additional_data(client, receiveFloats):
    return receiveFloats(client, 1)

# Forever loop will be halted by VREP client or by exception
while True:

    """
    In a closed loop, receive telemetry data from drone (position, acceleration etc.)
    and demands from the controller (hand-held(rx) or autonomous) and compute the thrust,
    that are sent back to the client (drone).
    """
    try:

        currtime = time.time()
        print(currtime - prevtime)
        prevtime = currtime

        # Get core data from client (the drone)
        core_data = Util.receive_floats(client, 4)

        # Quit on timeout
        if not core_data: exit(0)

        # Get extra data from client
        extraData = get_additional_data(client, Util.receive_floats)

        # Unpack IMU data        
        timestep = core_data[0]  # seconds
        pitch    = core_data[1]  # positive = nose up
        roll     = core_data[2]  # positive = right down
        yaw      = core_data[3]  # positive = nose right

        # Poll controller
        demands = controller.poll()

        # Get motor thrusts from quadrotor model
        thrusts = fmu.get_motors((pitch, roll, yaw), demands, timestep, extraData)

        # Send thrusts to client
        Util.send_floats(client, thrusts)

    except Exception:

        # Inform and exit on exception
        controller.error()
        exit(0)


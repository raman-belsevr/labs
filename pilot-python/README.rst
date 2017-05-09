PILOT module mimics an on-flight human pilot responsible for taking all actions related to flight control. 

Actions include pre-defined maneuvers such as take-off, cruise, change flight direction, landing etc, as well as data communication to and from the flight. A complete list will be generated in the final spec. These actions are initiated in two ways: a) governed by the flying conditions or surroundings of the flight, e.g. pilot changes direction if an obstacle lies in the immediate flight path, and b) based on specific instructions from the ATC (Air Traffic Controller), e.g. alter flight path, take photos or provide live video stream.

PILOT module fully understands flight dynamics such as yaw, pitch and roll.

PILOT module is implemented in python and interfaces with the services provided on-board by the computer. An intermediate layer called HAL (Hardware Abstraction Layer) existing between the PILOT and the on-board computer allows emulation of the on-board computer, a method useful for local testing of the PILOT module.

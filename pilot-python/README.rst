PILOT module mimics an on-flight human pilot responsible for taking all actions related to flight control. Note that Pilot 
is likely to receive instructions from the ATC (Air Traffic Controller), examples of which may include alteration to flight path,
request for flight metadata (or parameters), or directive to take photo or provide live stream. 

PILOT module is implemented in python an interfaces with the services provided on-board by the computer. Between the PILOT and the on-board 
computer, exists an intermediate layer called HAL (Hardware Abstraction Layer) that allows emulation of the on-board computer, a method
useful for local testing of the PILOT module.

PILOT module understands pre-defined maneuvres such as take-off, cruise and landing as well as understand flight dynamics (yaw, pitch, roll)
Any of the above actions can be initiated (or aborted) by the PILOT in response to flying conditions or by direction of the ATC.

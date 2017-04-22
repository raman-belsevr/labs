The DRONE module is responsible for proving APIs/Services that allow the PILOT module to manage the flight and maneouver the drone.
An example of a service/API would be to climb up at a given acceleration. The translation of the intent into actual changes in thrust
applied to the motors is an internal detail managed and hidden inside the the DRONE module. Thus a flight can be managed
by use of very high-level APIs, implementation of which is specific to a carrier (flying object) type. E.g. a surface vehicle may throw
and unsupported operation exception underneathe the climb up API. 

The DRONE module is written in python.

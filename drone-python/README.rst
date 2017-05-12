The DRONE module is responsible for providinng APIs/Services that allow the PILOT module to manage the flight and maneouver the drone.

An example of a API/service would be to climb up at a given acceleration. The DRONE module encapsulates the actual physical mechanism required to fulfil the service, e.g. the actual changes in thrust needed to be applied to the motors to achieve a specified flying condition pertaining to the service, is managed by the DRONE module. Thus a flight can be managed by use of very high-level APIs, implementation of which is specific to a carrier (flying object) type, e.g. a surface vehicle (designed to navigate on a 2D plane) may throw an unsupported operation exception underneath the climb up API. 

The DRONE module is written in python.

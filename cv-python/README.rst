CV module stands for Computer-Vision module and provides functionality for processing of images or video captured by the on-board camera. 
The CV module (implemented in python) may be required to process in near real-time or/and persist metadata (and data) on the on-board database
for subsequent retrieval in future (as requested by PILOT or ATC). 

CV module interfaces with the on-board camera using a HAL (Hardware Abstraction Layer) that acts as a layer of indirection, thus allowing
for emulation. 

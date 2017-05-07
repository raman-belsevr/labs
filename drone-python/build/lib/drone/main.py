import sys
from raspi.fc.flight_sequences import hover_sequence
from drone.drone_system import DroneSystem


def main():
    """Main entry point to the pilot system"""
    drone = DroneSystem("my_drone")
    flight_sequence = hover_sequence()

if __name__ == '__main__':
    sys.exit(main())
import sys
from raspi.fc.flight_sequences import hover_sequence
from pilot.pilot_model import Pilot


def main():
    """Main entry point to the pilot system"""
    pilot = Pilot()
    flight_sequence = hover_sequence()
    pilot.execute_flight_sequence(flight_sequence)


if __name__ == '__main__':
    sys.exit(main())
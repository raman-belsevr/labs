import sys
from raspi.fc.flight_sequences import hover_sequence
from raspi.fc.flight_sequences import climb_hover_descent_grounded
from raspi.raspi_logging import get_logger
from pilot.pilot_model import Pilot


def main():
    """Main entry point to the pilot system"""

    logger = get_logger(__name__)
    pilot = Pilot()
    flight_sequence = climb_hover_descent_grounded()
    pilot.execute_flight_sequence(flight_sequence)

if __name__ == '__main__':
    sys.exit(main())
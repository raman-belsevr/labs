from raspi.fc.flight_state_machine import ClimbFlightState
from raspi.fc.flight_state_machine import DescendFlightState
from raspi.fc.flight_state_machine import FlightSequence
from raspi.fc.flight_state_machine import FlightStage
from raspi.fc.flight_state_machine import GroundedFlightState
from raspi.fc.flight_state_machine import HoverFlightState


def climb_hover_descent_grounded():
    climb = FlightStage(ClimbFlightState(100), 10)
    hover = FlightStage(HoverFlightState(), 10)
    descend = FlightStage(DescendFlightState(), 10)
    grounded = FlightStage(GroundedFlightState())
    sequence = FlightSequence(list(climb, hover, descend, grounded))
    return sequence


def hover_sequence():
    hover = FlightStage(HoverFlightState(), 10)
    sequence = FlightSequence(list(hover))
    return sequence


def grounded_sequence():
    grounded = FlightStage(GroundedFlightState(), 10)
    sequence = FlightSequence(list(grounded))
    return sequence

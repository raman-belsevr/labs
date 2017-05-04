from drone.flight_state_machine import FlightStage
from drone.flight_state_machine import FlightSequence
from drone.flight_state_machine import ClimbFlightState
from drone.flight_state_machine import HoverFlightState
from drone.flight_state_machine import DescendFlightState
from drone.flight_state_machine import GroundedFlightState


def climb_hover_descent_grounded():
    climb = FlightStage(ClimbFlightState(100), 10)
    hover = FlightStage(HoverFlightState(), 10)
    descend = FlightStage(DescendFlightState(), 10)
    grounded = FlightStage(GroundedFlightState())

    sequence = FlightSequence(list(climb, hover, descend, grounded))
    return sequence



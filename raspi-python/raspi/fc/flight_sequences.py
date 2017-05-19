from raspi.fc.flight_state_machine import ClimbFlightState
from raspi.fc.flight_state_machine import DescendFlightState
from raspi.fc.flight_state_machine import FlightSequence
from raspi.fc.flight_state_machine import FlightStage
from raspi.fc.flight_state_machine import GroundedFlightState
from raspi.fc.flight_state_machine import HoverFlightState


def climb_hover_descent_grounded():
    climb = FlightStage(ClimbFlightState(5), 5)
    hover = FlightStage(HoverFlightState(), 5)
    descend = FlightStage(DescendFlightState(5), 5)
    grounded = FlightStage(GroundedFlightState(), 5)
    stage_list = list()
    stage_list.append(climb)
    stage_list.append(hover)
    stage_list.append(descend)
    stage_list.append(grounded)
    sequence = FlightSequence(stage_list)
    return sequence


def hover_sequence():
    hover = FlightStage(HoverFlightState(), 10)
    stage_list = list()
    stage_list.append(hover)
    sequence = FlightSequence(stage_list)
    return sequence


def grounded_sequence():
    grounded = FlightStage(GroundedFlightState(), 10)
    stage_list = list()
    stage_list.append(grounded)
    sequence = FlightSequence(stage_list)
    return sequence


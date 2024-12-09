from erlang_queue_calculator.AxisToModify import AxisToModify
from erlang_queue_calculator.DesiredSimulationOutcome import DesiredSimulationOutcome
from erlang_queue_calculator.MMCKParameters import MMCKParameters

class SimulationParameters:
    def __init__(self, starting_parameters: MMCKParameters, axis_to_modify: AxisToModify, desired_simulation_outcome: DesiredSimulationOutcome):
        self.starting_parameters = starting_parameters
        self.axis_to_modify = axis_to_modify
        self.desired_simulation_outcome = desired_simulation_outcome
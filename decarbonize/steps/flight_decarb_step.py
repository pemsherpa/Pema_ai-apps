
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class FlightDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, num_stops):
        super().__init__(DecarbStepType.FLIGHTS, cur_cost, new_cost, cur_emissions, new_emissions, description)
        self.num_stops = num_stops

    def generate_step_description(self):
        base_description = super().generate_step_description()
        return f"{base_description}, with {self.num_stops} stop(s)"

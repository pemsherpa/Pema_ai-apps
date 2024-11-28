
from abc import abstractmethod
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class FlightDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, num_stops, difficulty,transition_percentage):
        super().__init__(DecarbStepType.FLIGHTS, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty,transition_percentage)
        self.num_stops = num_stops
 
    def step_to_dict(self):
        dict = super().step_to_dict()
        dict['data'] = {
            'stops':self.num_stops
        }

        return dict
    def generate_step_description(self):
        base_description = super().generate_step_description()
        return f"{base_description}, with {self.num_stops} stop(s)"

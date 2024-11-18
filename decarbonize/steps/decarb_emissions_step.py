from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class FlightOptimizerDecarbStep(DecarbStep):

    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty, num_stops):
        super().__init__(DecarbStepType.FLIGHT_OPTIMIZER, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)
        self.num_stops = num_stops  # Ensure num_stops is properly initialized

    def step_to_dict(self):
        # Call the parent class's step_to_dict
        dict = super().step_to_dict()
        # Add additional data specific to this step
        dict['data'] = {
            'stops': self.num_stops
        }
        return dict

        

    
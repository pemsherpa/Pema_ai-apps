from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class FlightOptimizerDecarbStep(DecarbStep):

    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty):
        super().__init__(DecarbStepType.FLIGHT_OPTIMIZER, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)
    def step_to_dict(self):
        dict = self.step_to_dict()
        dict['data'] = {
            'stops':self.num_stops
        }
        # by switching 1st to economy, you save ... carbon
        # by decreasing num of flights, you save ... carbon
        # 1 and 2 can carpool...(display)
        # by taking bus/subway you can save... dollar and ... carbon

    
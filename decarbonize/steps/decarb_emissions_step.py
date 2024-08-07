from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class EmissionsDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty):
        super().__init__(DecarbStepType.EMISSIONS_FLIGHTS, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)
        

    
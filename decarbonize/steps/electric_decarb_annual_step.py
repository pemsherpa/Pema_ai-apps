from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class ElectricDecarbAnnualStep(DecarbStep):
    def __init__(self, rec, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty):
        super().__init__(DecarbStepType.ELECTRICITY_ANNUAL, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)
        self.rec = rec

        
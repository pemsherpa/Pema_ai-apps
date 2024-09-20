from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class ElectricDecarbAnnualStep(DecarbStep):
    def __init__(self, rec, e_step):
        super().__init__(DecarbStepType.ELECTRICITY_ANNUAL, e_step.cur_cost, e_step.new_cost, e_step.cur_emissions, e_step.new_emissions, e_step.description, e_step.difficulty)
        self.rec = rec

    def step_to_dict(self):
        dict = super().step_to_dict()
        dict['data'] = {
            'newdata gowri': "FIX STRING"
        }
        return dict
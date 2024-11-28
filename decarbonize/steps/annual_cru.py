from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class CRUAnnualStep(DecarbStep):
    def __init__(self, rec,cru_step):
        super().__init__(DecarbStepType.CRU_ANNUAL, cru_step.cur_cost, cru_step.new_cost, cru_step.cur_emissions, cru_step.new_emissions, cru_step.description, cru_step.difficulty,cru_step.transition_percentage)
        self.rec=rec

    def step_to_dict(self):
        dict = super().step_to_dict()
        dict['recommendation'] = self.rec
        return dict
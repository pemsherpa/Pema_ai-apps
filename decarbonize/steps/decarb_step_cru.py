from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class CRUDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, CRU_amount, difficulty,transition_percentage):
        super().__init__(DecarbStepType.CRU, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty,transition_percentage)
        self.CRU_amount = CRU_amount

    def step_to_dict(self):
        dict = super().step_to_dict()
        dict['recommendations'] = {
            'CRU_amount': self.CRU_amount
        }

        return dict

    def generate_step_description(self):
        base_description = super().generate_step_description()
        return f"{base_description}, with CRU amount: {self.CRU_amount}"

# Additional Decarb_CRU Class Implementation
class Decarb_CRU(CRUDecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, CRU_amount, difficulty, timeframe,transition_percentage):
        super().__init__(cur_cost, new_cost, cur_emissions, new_emissions, description, CRU_amount, difficulty,transition_percentage)
        self.timeframe = timeframe

    

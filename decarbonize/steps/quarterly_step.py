from steps.decarb_step import DecarbStepType
from steps.electric_decarb_annual_step import ElectricDecarbAnnualStep
from steps.electric_decarb_step import ElectricDecarbStep

class QuarterStep:
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter
        self.scope1_steps = []
        self.scope2_steps = [] 
        self.scope3_steps = []

    def add_step(self, step):
        # Add step based on its scope
        if step.scope == 1:
            self.scope1_steps.append(step)
        elif step.scope == 2:
            self.scope2_steps.append(step)
        elif step.scope == 3:
            self.scope3_steps.append(step)

    def add_rec_to_scope2(self, e_step, rec):
        if not (type(e_step) is ElectricDecarbStep):
            raise TypeError(f"add_rec_to_scope2: Unexpected step type: {type(e_step)}")  
        
        e_annual_step = ElectricDecarbAnnualStep(rec, e_step.cur_cost, e_step.new_cost, e_step.cur_emissions, e_step.new_emissions, e_step.description, e_step.difficulty)
        print("add_rec_to_scope2")
        self.scope2_steps.append(e_annual_step)

    def to_dict(self):
        return {
            "year": self.year,
            "quarter": self.quarter,
            "scope1_steps": [self._convert_step(step) for step in self.scope1_steps],
            "scope2_steps": [self._convert_step(step) for step in self.scope2_steps],
            "scope3_steps": [self._convert_step(step) for step in self.scope3_steps],
        }

    def _convert_step(self, step):
        if isinstance(step, dict):
            return step  # If step is already a dictionary, return it as is
        elif hasattr(step, 'step_to_dict'):
            return step.step_to_dict()  # Use the step's method to convert to a dictionary
        else:
            raise TypeError(f"Unexpected step type: {type(step)}")  # Handle unexpected types




        
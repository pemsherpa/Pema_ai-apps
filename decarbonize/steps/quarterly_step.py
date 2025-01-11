from steps.decarb_step import DecarbStepType
from steps.electric_decarb_annual_step import ElectricDecarbAnnualStep
from steps.electric_decarb_step import ElectricDecarbStep
from steps.annual_cru import CRUAnnualStep
from steps.decarb_step_cru import CRUDecarbStep

class QuarterStep:
    def __init__(self, company_id,year, quarter):
        self.company_id=company_id
        self.year = year
        self.quarter = quarter
        self.scope1_steps = []
        self.scope2_steps = [] 
        self.scope3_steps = []

    def add_step(self, step):
        # Add step based on its scope
        if step.scope == 1:
            self.scope1_steps.append(step)
        # elif step.scope == 2:
        #     self.scope2_steps.append(step)
        # elif step.scope == 3:
        #     self.scope3_steps.append(step)

    def add_electric_step(self, e_rec, e_step):
        e_annual_step = ElectricDecarbAnnualStep(e_rec, e_step)
        self.scope2_steps.append(e_annual_step)

    def add_cru_step(self,cru_rec,cru_step):
        cru_annual= CRUAnnualStep(cru_rec,cru_step)
        self.scope3_steps.append(cru_annual)

    def add_flight_step(self,flight_step):
        self.scope3_steps.append(flight_step)

    def add_commute_step(self,commute_step):
        self.scope3_steps.append(commute_step)

    def add_flight_step(self,flight_step):
        self.scope3_steps.append(flight_step)

    def add_rec_to_scope2(self, e_step, rec):
        if not (type(e_step) is ElectricDecarbStep):
            raise TypeError(f"add_rec_to_scope2: Unexpected step type: {type(e_step)}")  
        
        e_annual_step = ElectricDecarbAnnualStep(rec, e_step.cur_cost, e_step.new_cost, e_step.cur_emissions, e_step.new_emissions, e_step.description, e_step.difficulty,e_step.transition_percentage)
        print("add_rec_to_scope2")
        self.scope2_steps.append(e_annual_step)

    def add_rec_to_scope3(self, cru_step, rec):
        if not (type(cru_step) is CRUDecarbStep):
            raise TypeError(f"add_rec_to_scope2: Unexpected step type: {type(cru_step)}")  
        
        cru_annual_step = CRUAnnualStep(rec, cru_step.cur_cost, cru_step.new_cost, cru_step.cur_emissions, cru_step.new_emissions, cru_step.description, cru_step.difficulty,cru_step.transition_percentage)
        print("add_rec_to_scope3")
        self.scope2_steps.append(cru_annual_step)
        
    def to_dict(self,company_id):
        return {
            "company_id":self.company_id,
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
        # else:
        #     raise TypeError(f"Unexpected step type: {type(step)}")  # Handle unexpected types
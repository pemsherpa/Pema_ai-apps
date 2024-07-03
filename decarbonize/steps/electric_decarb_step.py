
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class ElectricDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_renewable, new_renewable, kwh_used, description):
        self.cur_renewable=cur_renewable
        self.new_renewable =new_renewable
        self.kwh_used = kwh_used
        cur_emissions = self.get_carbon_from_electric(kwh_used)
        new_emissions = self.get_new_carbon_from_electric(cur_emissions, cur_renewable, new_renewable)
        super().__init__(DecarbStepType.ELECTRICITY, cur_cost, new_cost, cur_emissions, new_emissions, description)

    def generate_step_description(self):
        base_description = super().generate_step_description()
        return f"{base_description}"
    
    def get_carbon_from_electric(self, kwh_used):
        # Make API request for electric
        # TODO fix with API call
        return kwh_used * 1.5

    def get_new_carbon_from_electric(self, cur_emissions, cur_renewable, new_renewable):
        cur_emissions = cur_emissions * (new_renewable - cur_renewable)
        return cur_emissions
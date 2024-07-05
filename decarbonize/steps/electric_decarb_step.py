
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class ElectricDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_renewable, new_renewable, kwh_used, description, difficulty):
        self.cur_renewable = cur_renewable
        self.new_renewable = new_renewable
        self.kwh_used = kwh_used
        cur_emissions = self.get_carbon_from_electric(kwh_used)
        new_emissions = self.get_new_carbon_from_electric(cur_emissions, cur_renewable, new_renewable)
        super().__init__(DecarbStepType.ELECTRICITY, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)

    def get_cur_cost(self):
        user_zip_code = 95347
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', user_zip_code)
        user_current_plan = 'B19_SV'
        cur_cost = ce.check_condition_and_run(user_current_plan)
        self.steps.append(cur_cost)
        return cur_cost

    def get_new_cost(self):
        user_zip_code = 95347
        ew = ElectricityWork('Electricity Rate Plan.xlsx', user_zip_code)
        
        user_sector = 'Large Commercial and Industrial'
        user_bundled = 'Yes'
        new_cost = ew.check_condition_and_run(user_sector, user_bundled)
        self.steps.append(new_cost)
        return new_cost

    def compute_electricbill_savings(self):
        current_electricbill_price = 10000
        return (self.cur_cost - self.new_cost)/self.cur_cost * current_electricbill_price

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

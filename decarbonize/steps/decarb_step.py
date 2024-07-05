
class DecarbElectricStep:
    def __init__(self, step_type, user_current_plan, cur_cost, new_cost,  cur_renewable, new_renewable, description, difficulty):
        self.step_type = step_type
        self.cur_cost = cur_cost
        self.new_cost = new_cost
        self.cur_emissions = cur_emissions
        self.new_emissions = new_emissions
        self.description = description
        self.difficulty = difficulty
        self.user_current_plan = user_current_plan
        
    def get_cur_cost(self):
        user_zip_code = 95347
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', user_zip_code)
        user_current_plan = 'B19SVB'
        new_cost = ce.check_condition_and_run(user_current_plan)
        self.steps.append(new_cost)
        return cur_cost

    
    def get_new_cost(self):
        user_zip_code = 95347
        ew = ElectricityWork('Electricity Rate Plan.xlsx', user_zip_code)
        
        user_sector = 'Large Commercial and Industrial'
        user_bundled = 'Yes'
        user_current_plan = 'B19SVB'
        new_cost = ew.check_condition_and_run(user_sector, user_bundled)
        self.steps.append(new_cost)
        return new_cost

    def compute_zscore(self):
        # (cost savings, carbon savings, difficulty)
        self.cost_savings = self.compute_savings()
        self.emission_savings = self.compute_emissions_savings()
        #TODO: Tunan compute ZScore
        self.ranking_zscore = self.difficulty 

    def compute_savings(self):
        return self.cur_cost - self.new_cost

    def compute_emissions_savings(self):
        return self.cur_emissions - self.new_emissions

    def generate_step_description(self):
        return f"Step {self.step_type.value}: {self.description}"


from components.electricity.current_price_calculation.current_electricity import CurrentElectricity
from components.electricity.optimization_calculation.electricity_work import ElectricityWork




class DecarbStep:
    def __init__(self, step_type, cur_cost, new_cost,cur_emissions,new_emissions,description,ranking_zscore):
        self.step_type = step_type
        self.cur_cost = cur_cost
        self.new_cost = new_cost
        self.cur_emissions = 1
        self.new_emissions = 1
        self.ranking_zscore = ranking_zscore

        
    def get_cur_cost(self):
        user_zip_code = 95347
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', user_zip_code)
        user_current_plan = 'B19SVB'
        new_cost = ce.check_condition_and_run(user_current_plan)
        self.steps.append(new_cost)
        return self.cur_cost

    
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

        
        self.ranking_zscore = (self.difficulty + self.cost_savings + self.emission_savings)/3

    def compute_savings(self):
        return self.cur_cost - self.new_cost

    def compute_emissions_savings(self):
        return self.cur_emissions - self.new_emissions

    def generate_step_description(self):
        return f"Step {self.step_type.value}: {self.description}"

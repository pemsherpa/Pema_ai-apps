from components.electricity.current_price_calculation.current_electricity import CurrentElectricity
from components.electricity.optimization_calculation.electricity_work import ElectricityWork

class DecarbStep:
    def __init__(self, step_type, cur_cost, new_cost,cur_emissions,new_emissions,description,difficulty):
        self.step_type = step_type
        self.cur_cost = cur_cost
        self.new_cost = new_cost
        self.cur_emissions = cur_emissions
        self.new_emissions = new_emissions
        self.description = description
        self.difficulty = difficulty

    def get_cur_cost(self):
        return self.cur_cost
    
    def get_new_cost(self):
        return self.new_cost

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


from abc import abstractmethod
from steps.decarb_step_type import DecarbStepType


class DecarbStep:
    def __init__(self, step_type: DecarbStepType, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty,transition_percentage):
        self.step_type = step_type
        self.cur_cost = cur_cost
        self.new_cost = new_cost
        self.cur_emissions = cur_emissions
        self.new_emissions = new_emissions
        self.description = description
        self.difficulty = difficulty
        self.transition_percentage=transition_percentage
       
        scope_mapping = {
            DecarbStepType.ELECTRICITY: 2,
            DecarbStepType.ELECTRICITY_ANNUAL: 2,
            DecarbStepType.COMMUTING_CARPOOL: 3,
            DecarbStepType.COMMUTING_INDIVIDUAL: 3,
            DecarbStepType.FLIGHTS: 3,
            DecarbStepType.FLIGHTS_RETURN: 3,
            DecarbStepType.CRU: 3,
            DecarbStepType.CRU_ANNUAL:3,
            DecarbStepType.FLIGHT_OPTIMIZER: 3,
        }
        #Transition percentage of each step: Must be added in decarb step
        self.scope = scope_mapping.get(step_type)
        if self.scope is None:
            print(f"Unhandled step type: {step_type}")
            raise ValueError(f'Step type {step_type} not handled')

    def step_to_dict(self):
        return {
            "description": self.generate_step_description(),
            "difficulty": self.difficulty,
            "savings": self.compute_savings(),
            "emissions_savings": self.compute_emissions_savings(),
            "transition_percentage":self.generate_transiton_percentage()
        }

    def compute_savings(self):
        print("compute_savings")
        print(f"{self.cur_cost } {self.new_cost}")
        return self.cur_cost - self.new_cost

    def compute_emissions_savings(self):
        return self.cur_emissions - self.new_emissions

    def compute_zscore(self, value, mean, std):
        if std == 0:
            return 0
        return (value - mean) / std

    def compute_ranking_zscore(self, mean_diff, std_diff, mean_savings, std_savings, mean_emissions, std_emissions):
        z_difficulty = self.compute_zscore(self.difficulty, mean_diff, std_diff)
        z_savings = self.compute_zscore(self.compute_savings(), mean_savings, std_savings)
        z_emissions = self.compute_zscore(self.compute_emissions_savings(), mean_emissions, std_emissions)
        
        self.ranking_zscore = (z_difficulty + z_savings + z_emissions) / 3
        return self.ranking_zscore

    def generate_step_description(self):
        return f"{self.description}"
    
    def generate_transiton_percentage(self):
        return self.transition_percentage
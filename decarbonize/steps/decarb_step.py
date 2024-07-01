
class DecarbStep:
    def __init__(self, step_type, cur_cost, new_cost, cur_emissions, new_emissions, description, ranking_zscore):
        self.step_type = step_type
        self.cur_cost = cur_cost
        self.new_cost = new_cost
        self.cur_emissions = cur_emissions
        self.new_emissions = new_emissions
        self.description = description
        self.ranking_zscore = ranking_zscore

    def compute_savings(self):
        return self.cur_cost - self.new_cost

    def compute_emissions_savings(self):
        return self.cur_emissions - self.new_emissions

    def generate_step_description(self):
        return f"Step {self.step_type.value}: {self.description}"

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
    
    def compute_zscore(self,x,mean,std):
        if std == 0:
            return 0
        z_score = (x - mean) / std
        return z_score
    
    def compute_ranking_zscore(self,mean_diff, std_diff, mean_savings, std_savings, mean_emissions, std_emissions):
        z_difficulty = self.compute_zscore(self.difficulty, mean_diff, std_diff)
        z_savings = self.compute_zscore(self.compute_savings(), mean_savings, std_savings)
        z_emissions = self.compute_zscore(self.compute_emissions_savings(), mean_emissions, std_emissions)
        
        self.ranking_zscore = (z_difficulty + z_savings + z_emissions) / 3

        return self.ranking_zscore

    def compute_savings(self):
        return self.cur_cost - self.new_cost

    def compute_emissions_savings(self):
        return self.cur_emissions - self.new_emissions

    def generate_step_description(self):
        return f"Step {self.step_type.value}: {self.description}"

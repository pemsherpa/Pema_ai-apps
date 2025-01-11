from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class DecarbCommuteStep(DecarbStep):
    def __init__(self, step_type, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty, transition_percentage, commute_steps):
        super().__init__(DecarbStepType.COMMUTING_CARPOOL, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty, transition_percentage)
        self.commute_steps = commute_steps
    
    def to_json(self):
        json_output = []
        
        # Iterate over each CommuteStep in commute_steps
        for commute_step in self.commute_steps:
            recommendation = {
                "group": commute_step.group,
                "members": commute_step.members,
                "message": "Solo rider - no savings possible." if len(commute_step.members) == 1 else None,
                "money_saving": 0 if len(commute_step.members) == 1 else commute_step.savings,
                "emission_saving": 0 if len(commute_step.members) == 1 else commute_step.savings_emissions,
                "distance_saving": 0 if len(commute_step.members) == 1 else commute_step.saving_distance,
            }
            json_output.append(recommendation)
        
        return json_output
  
    def step_to_dict(self):
        dict = super().step_to_dict()
        # Fix here: call self.to_json() instead of just to_json()
        dict['commute_step_recommendations'] = self.to_json()  # Add the JSON output to the dictionary
        return dict

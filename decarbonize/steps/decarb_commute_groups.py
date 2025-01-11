class CommuteStep:
    def __init__(self, group, members, savings, savings_emission, saving_distance):
        self.group = group
        self.members = members
        self.savings = savings
        self.savings_emissions = savings_emission
        self.saving_distance = saving_distance
    
    def to_json(self):
        # Construct the recommendation part
        recommendation = {
            "group": self.group,
            "members": self.members,
            "message": "Solo rider - no savings possible." if len(self.members) == 1 else None,
            "money_saving": 0 if len(self.members) == 1 else self.savings,
            "emission_saving": 0 if len(self.members) == 1 else self.savings_emissions,
            "distance_saving": 0 if len(self.members) == 1 else self.saving_distance,
        }
        return recommendation
    




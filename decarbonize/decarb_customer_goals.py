

import math
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class DecarbCustomerGoals():
    
    def __init__(self, timeframe,customer_id, year, scope1_emissions, scope2_emissions, scope3_emissions, scope1_target, scope2_target, scope3_target):
        self.timeframe = timeframe
        self.customer_id = customer_id
        self.year = year
        self.scope1_emissions = scope1_emissions
        self.scope2_emissions = scope2_emissions
        self.scope3_emissions = scope3_emissions
        
        if scope1_target < 0 or scope1_target > 1:
            raise ValueError (f"Scope1 target must be between 0 and 1!{scope1_target}")
        if scope2_target < 0 or scope2_target > 1:
            raise ValueError (f"Scope2 target must be between 0 and 1!{scope2_target}")
        if scope3_target < 0 or scope3_target > 1:
            raise ValueError (f"Scope3 target must be between 0 and 1!{scope3_target}")
        
        self.scope1_target = scope1_target
        self.scope2_target = scope2_target
        self.scope3_target = scope3_target

    def create_yearly_goals(self):
        yearly_goals = []
        current_year = self.year

        for i in range(self.timeframe):
            
            factor = math.exp(-i / self.timeframe)
            yearly_goal = {
                "year": current_year,
                "scope1_goal": self.scope1_emissions * (1 - self.scope1_target * factor),
                "scope2_goal": self.scope2_emissions * (1 - self.scope2_target * factor),
                "scope3_goal": self.scope3_emissions * (1 - self.scope3_target * factor),
            }
            yearly_goals.append(yearly_goal)
            current_year += 1

        return yearly_goals
        

    


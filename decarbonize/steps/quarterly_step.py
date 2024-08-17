class QuaterStep:
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter
        self.scope1_steps = []  #
        self.scope2_steps = [] 
        self.scope3_steps = []  

    def add_step(self, step):
        # Add step based on its scope
        if step.scope == 1:
            self.scope1_steps.append(step)
        elif step.scope == 2:
            self.scope2_steps.append(step)
        elif step.scope == 3:
            self.scope3_steps.append(step)

    def to_dict(self):
        return {
            "year": self.year,
            "quarter": self.quarter,
            "scope1_steps": [step.step_to_dict() for step in self.scope1_steps],
            "scope2_steps": [step.step_to_dict() for step in self.scope2_steps],
            "scope3_steps": [step.step_to_dict() for step in self.scope3_steps],
        }



        
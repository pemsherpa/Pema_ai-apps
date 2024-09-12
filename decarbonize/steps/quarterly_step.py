from steps.decarb_step import DecarbStepType

class QuarterStep:
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter
        self.scope1_steps = []
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
            "scope1_steps": [self._convert_step(step) for step in self.scope1_steps],
            "scope2_steps": [self._convert_step_with_recommendations(step) for step in self.scope2_steps],
            "scope3_steps": [self._convert_step(step) for step in self.scope3_steps],
        }

    def _convert_step(self, step):
        if isinstance(step, dict):
            return step  # If step is already a dictionary, return it as is
        elif hasattr(step, 'step_to_dict'):
            return step.step_to_dict()  # Use the step's method to convert to a dictionary
        else:
            raise TypeError(f"Unexpected step type: {type(step)}")  # Handle unexpected types

    def _convert_step_with_recommendations(self, step):
        step_dict = self._convert_step(step)
        if hasattr(step, 'recommendations') and step.recommendations:
            # Add recommendations to the step dictionary
            step_dict['recommendations'] = step.recommendations
        return step_dict




        
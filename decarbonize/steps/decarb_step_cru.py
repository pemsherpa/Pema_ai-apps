from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType


class Decarb_CRU(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description,  difficulty,timeframe):
        super().__init__(DecarbStepType.FLIGHTS, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)
        self.timeframe = timeframe



    
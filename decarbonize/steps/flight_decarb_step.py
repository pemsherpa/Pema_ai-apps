
from abc import abstractmethod
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class FlightDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description,num_stops, difficulty, transition_percentage, is_round_trip,travel_class, departure_airport, arrival_airport):
        super().__init__(
            step_type=DecarbStepType.FLIGHTS,
            cur_cost=cur_cost,
            new_cost=new_cost,
            cur_emissions=cur_emissions,
            new_emissions=new_emissions,
            description=description,
            difficulty=difficulty,
            transition_percentage=transition_percentage
        )
        self.scope = 3 
        self.num_stops = num_stops
        self.is_round_trip = is_round_trip
        self.travel_class = travel_class
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport

    def step_to_dict(self):
        return {
            "cur_cost": self.cur_cost,
            "new_cost": self.new_cost,
            "cur_emissions": self.cur_emissions,
            "new_emissions": self.new_emissions,
            "description": self.description,
            "difficulty": self.difficulty,
            "transition_percentage": self.transition_percentage,
            "data": {
                "is_round_trip": self.is_round_trip,
                "travel_class": self.travel_class,
                "departure_airport": self.departure_airport,
                "arrival_airport": self.arrival_airport,
                "num_stops": self.num_stops
            }
        }


from abc import abstractmethod
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class FlightDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_emissions, new_emissions, description, num_stops, difficulty, transition_percentage, is_round_trip, travel_class, departure_airport, arrival_airport):
        super().__init__(DecarbStepType.FLIGHTS, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty, transition_percentage)
        self.num_stops = num_stops
        self.is_round_trip = is_round_trip
        self.travel_class = travel_class
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport

    def step_to_dict(self):
        dict = super().step_to_dict()
        return dict
    
    def generate_step_description(self):
        base_description = super().generate_step_description()
        return f"{base_description}, with {self.num_stops} stop(s)"
    
    

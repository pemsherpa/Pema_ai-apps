# -*- coding: utf-8 -*-
"""DecarbEngine.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EWIicIg05wODK4aX-Dk-DY5WdoQz968r
"""

from components.biz_commute_analyzer import BusinessCommutingAnalyzer
from components.electric_bill_analyzer import ElectricityBillAnalyzer
from components.flight_data_analyzer import FlightDataAnalyzer
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType
from steps.decarb_weight import DecarbWeight
import pandas as pd
from itertools import permutations
from steps.flight_decarb_step import FlightDecarbStep

class DecarbEngine:
    def __init__(self, commuting_data,dynamic_data, origin, destination, departure_date,firm,weights,return_date=None):
        self.GOOGLE_MAPS_API_KEY = "AIzaSyD1fbsNKLIWwHly5YcSBcuMWhYd2kTIN08"
        self.FLIGHT_API_KEY = '7b97097f97bcea06b3c9c8b81e864da1f686069cdfba1dfd89834eec702b8f16'
        self.OIL_PRICE_API_KEY = 'jDLAcmPbuXd1CMXRjKFZMliukSgC6ujhUjnKaxOf'
        self.firm = firm
        self.dynamic = dynamic_data
        self.weights = weights

        self.commuting_analyzer = BusinessCommutingAnalyzer(commuting_data, self.GOOGLE_MAPS_API_KEY, self.OIL_PRICE_API_KEY,self.firm,self.dynamic)
        self.flight_analyzer = FlightDataAnalyzer(self.FLIGHT_API_KEY,self.weights, origin, destination, departure_date, return_date)
        self.steps = []

    def analyze_commuting_costs(self):
        return self.commuting_analyzer.calculate_current_costs_and_emissions()

    def analyze_flight_costs(self):
        return self.flight_analyzer.get_optimal_flight(self.flight_analyzer.df_all_flights)

    def get_return_flight_options(self):
        return self.flight_analyzer.get_return_tickets()

    def compare_flight_stops(self):
       return self.flight_analyzer.compare_stops()

    def non_economy_cheaper_than_economy(self):
       return self.flight_analyzer.non_economy_cheaper_than_economy()

    def get_price_insights(self):
       return self.flight_analyzer.price_insights()

    def run_decarb_engine(self):
        savings = 0

        # commuting costs and emissions for individual
        commuting_costs, commuting_emissions = self.analyze_commuting_costs()
        commuting_step = DecarbStep(
            step_type=DecarbStepType.COMMUTING,
            cur_cost=commuting_costs,

            new_cost=self.commuting_analyzer.stipent_individual(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location, 1,
                                                                 50, 2,30)[2],
            cur_emissions=commuting_emissions,
            new_emissions=commuting_emissions * 0.9,  # fake num
            description="Analyze commuting costs and emissions for individual"
        )
        self.steps.append(commuting_step)
        savings += commuting_step.compute_savings()

        # commuting cost for carpool
        commuting_costs, commuting_emissions = self.analyze_commuting_costs()
        commuting_step = DecarbStep(
            step_type=DecarbStepType.COMMUTING,
            cur_cost=commuting_costs,
            new_cost = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,
                                                                       [1,2,3], 50,2,30)[0],
            new_emissions = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,
                                                                       [1,2,3], 50,2,30)[2],
            cur_emissions=commuting_emissions,
            description="Analyze commuting costs and emissions for carpool"
        )
        self.steps.append(commuting_step)
        savings += commuting_step.compute_savings()
        
        #flight costs
        optimal_flight = self.analyze_flight_costs()
        print(optimal_flight)
        flight_step = self.create_flight_step(optimal_flight)
        self.steps.append(flight_step)
        savings += flight_step.compute_savings()

        # return flight
        return_flight = self.get_return_flight_options(self.weights)
        return_flight_step = self.create_flight_step(return_flight)
        self.steps.append(return_flight_step)
        savings += return_flight_step.compute_savings()

        return self.steps

    def create_flight_step(self, return_flight):
        return_flight_savings = return_flight['Price'].iloc[0]
        return_flight_emissions = return_flight['Carbon Emissions'].iloc[0]
        return_flight_step = FlightDecarbStep(
            step_type=DecarbStepType.FLIGHTS,
            cur_cost=return_flight_savings * 1.1, # fake
            new_cost=return_flight_savings,
            cur_emissions=return_flight_emissions * 1.1, # fake
            new_emissions=return_flight_emissions,
            description="Analyze return flight costs and emissions",
            num_stops=return_flight['Stops'].iloc[0]
        )
        return return_flight_step

def run_electric_main():
    providers = [
        {'name': 'Provider A', 'location': 'Location 1', 'cost_per_kwh': 0.15, 'carbon_per_kwh': 0.5},
        {'name': 'Provider B', 'location': 'Location 1', 'cost_per_kwh': 0.12, 'carbon_per_kwh': 0.4},
        {'name': 'Provider C', 'location': 'Location 2', 'cost_per_kwh': 0.10, 'carbon_per_kwh': 0.3},
        {'name': 'Provider D', 'location': 'Location 2', 'cost_per_kwh': 0.13, 'carbon_per_kwh': 0.2},
    ]

    # electricity bill
    electricity_bill = {
        'location': 'Location 1',
        'total_consumption_kwh': 500,
        'total_cost': 75  # Assume current provider's cost per kWh is 0.15
    }

    # historical data
    historical_data = [
        {'consumption_kwh': 450, 'cost': 67.5},
        {'consumption_kwh': 500, 'cost': 75},
        {'consumption_kwh': 480, 'cost': 72}
    ]

    # current tariff
    current_tariff = {
        'total_consumption_kwh': 500,
        'total_cost': 75,
        'peak_consumption_kwh': 300,
        'off_peak_consumption_kwh': 200
    }

    # new tariffs
    new_tariffs = [
        {'name': 'Tariff A', 'flat_rate': 0.14},
        {'name': 'Tariff B', 'peak_rate': 0.16, 'off_peak_rate': 0.08}
    ]

    # Create class
    analyzer = ElectricityBillAnalyzer(providers)

    # Get recommendations
    recommendations = analyzer.recommend_providers(electricity_bill)
    print("Provider Recommendations:")
    for recommendation in recommendations:
        print(recommendation)

    # Analyze historical data
    historical_analysis = analyzer.analyze_historical_data(historical_data)
    print("\nHistorical Data Analysis:")
    print(historical_analysis)

    # Compare tariffs
    tariff_comparisons = analyzer.compare_tariffs(current_tariff, new_tariffs)
    print("\nTariff Comparisons:")
    for comparison in tariff_comparisons:
        print(comparison)

    # Suggest carbon offsets
    carbon_savings = 200
    carbon_offset_suggestions = analyzer.suggest_carbon_offsets(carbon_savings)
    print("\nCarbon Offset Suggestions:")
    for suggestion in carbon_offset_suggestions:
        print(suggestion)

    # Notify
    analyzer.notify_user("tunan_li@berkely.edu", "We found a better electricity plan for you!")

    # Integrate with UI
    user_input = {'bill': electricity_bill}
    ui_recommendations = analyzer.integrate_with_ui(user_input)
    print("\nUI Integration Recommendations:")
    for recommendation in ui_recommendations:
        print(recommendation)

def run_commute_and_flight():
    origin = "LAX"
    destination = "JFK"
    departure_date = "2024-07-01"
    return_date = "2024-07-10"
    firm = '2107 Addison St, Berkeley, CA'
    commuting_data = pd.DataFrame({
        'ID': [1, 2, 3],
        'method':['car','uber','car'],
        'locations':['1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA '],
        'frequency': [22, 20, 18],
        'cost_per_km':[0.1,0.2,0.3]
    })

    df_dynamic = pd.DataFrame({
        'method': ['bus', 'train', 'uber'],
        'distance': [10, 10, 10],
        'cost_per_km': [0.1, 0.2, 0.7]
    })

    weights =  DecarbWeight(0.4, 0.3, 0.2, 0.1) 
    decarb_engine = DecarbEngine(commuting_data, df_dynamic,origin, destination, departure_date, firm, weights,return_date)
    decarb_steps = decarb_engine.run_decarb_engine()

    for step in decarb_steps:
        print(step.generate_step_description())
        print(f"Savings: ${step.compute_savings()}")
        print(f"Emissions Savings: {step.compute_emissions_savings()} kg CO2\n")

def main():
    run_commute_and_flight()
    # run_electric_main()
    


if __name__ == "__main__":
    main()
    
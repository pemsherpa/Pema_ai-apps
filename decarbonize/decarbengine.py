# -*- coding: utf-8 -*-
"""DecarbEngine.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EWIicIg05wODK4aX-Dk-DY5WdoQz968r
"""
import math
import datetime
import json
#import requests
from decarb_customer_goals import DecarbCustomerGoals
import numpy as np
from components.biz_commute_analyzer import BusinessCommutingAnalyzer
from steps.decarb_step_cru import Decarb_CRU
from steps.decarb_step_cru import CRUDecarbStep
from steps.electric_decarb_step import ElectricDecarbStep
from components.electricity.sectors.lcbsector import LCBSector_simplified
from components.electricity.sectors.lcusector import LCUSector_simplified
from components.electricity.sectors.smbsector import SMBSector_simplified
from components.electricity.sectors.smusector import SMUSector_simplified
from components.flight_data_analyzer import FlightDataAnalyzer
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType
from steps.decarb_weight import DecarbWeight
from steps.electric_recommendations import Electric_Recommendations
from steps.cru_recommendations import CRU_Recommendations
import pandas as pd
from steps.flight_decarb_step import FlightDecarbStep
from components.FlightEmissionsCalculator import FlightEmissionsCalculator
from components.FlightEmissionsCalculator import Flight
from steps.decarb_emissions_step import FlightOptimizerDecarbStep
from steps.quarterly_step import QuarterStep
from steps.provider_info import ProviderInfo
from steps.provider_info_cru import ProviderInfoCru
from steps.decarb_commute_step import DecarbCommuteStep
import sys
import os
import django

# Add the root directory of your project to the Python path
base_path = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
relative_path = os.path.join(base_path, '../Database_Django/database_cs')  # Adjust based on your folder structure
sys.path.append(os.path.normpath(relative_path))

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'database_cs.settings')

# Setup Django
django.setup()

from yearly_steps.models import *
# Import the required module
from yearly_steps.views_json_yearly import *

class DecarbEngine:
    def __init__(self, commuting_data,dynamic_data,firm,weights,pre_flight_cost,decarb_goals):
        self.GOOGLE_MAPS_API_KEY = "AIzaSyDNBM20_Bc2on1-q14X8NE-hWTa1imUhH4"
        self.FLIGHT_API_KEY = '07ca28add927e7dcc2756d7d2a88a0e164b6ef28cfa34ef3eb2f90ea5c9a4279' #Replaced the API Key on 24/01, by Aniketh
        self.OIL_PRICE_API_KEY = 'jDLAcmPbuXd1CMXRjKFZMliukSgC6ujhUjnKaxOf'
        self.COORDINATES_API_KEY = "7111777279e746248e1eea239d8ed555"   #Replaced the API Key on 17/01
        self.firm = firm
        self.dynamic = dynamic_data
        self.weights = weights
        self.pre_flight_cost = pre_flight_cost
        self.decarb_goals = decarb_goals

        self.emissions_df = FlightEmissionsCalculator("Emissions_Flights.xlsx", self.COORDINATES_API_KEY)
        self.commuting_analyzer = BusinessCommutingAnalyzer(commuting_data, self.GOOGLE_MAPS_API_KEY, self.OIL_PRICE_API_KEY,self.firm,self.dynamic)
        self.steps = []
        self.dict_zscore = {}

    def compute_zscore(self):
        difficulties = [step.difficulty for step in self.decarb_steps]
        savings = [step.compute_savings() for step in self.decarb_steps]
        emissions = [step.compute_emissions_savings() for step in self.decarb_steps]

        mean_diff = np.mean(difficulties)
        mean_savings = np.mean(savings)
        mean_emissions = np.mean(emissions)

        std_diff = np.std(difficulties)
        std_savings = np.std(savings)
        std_emissions = np.std(emissions)

        total_savings = 0
        total_emission_savings = 0
        total_zscore = 0
        
        for step in self.decarb_steps:
            this_savings = step.compute_savings()
            this_emission_savings = step.compute_emissions_savings()
            total_savings += this_savings
            total_emission_savings += this_emission_savings
            this_z_score = step.compute_ranking_zscore(mean_diff, std_diff, mean_savings, std_savings, mean_emissions, std_emissions)
            total_zscore += this_z_score
            this_step_type = step.step_type.name
            self.dict_zscore[this_step_type] = this_z_score

            print(step.generate_step_description())
            print(f"z-score is: {self.dict_zscore[this_step_type]}")
            print(f"Difficulty: {step.difficulty}")  
            print(f"Savings: ${this_savings}")
            print(f"Emissions Savings: {this_emission_savings} kg CO2\n")
        
        num_steps = len(self.decarb_steps)
        if num_steps > 0:
            self.dict_zscore["avg-zscore"] = total_zscore / num_steps
        else:
            self.dict_zscore["avg-zscore"] = 0
        print(f"Total Savings: ${total_savings}")
        print(f"Total Emissions Savings: {total_emission_savings} kg CO2\n")

    def analyze_commuting_costs(self):
        return self.commuting_analyzer.calculate_current_costs_and_emissions()
    
    def run_commuting_step(self):
        # commuting costs and emissions for individual
     commuting_costs, commuting_emissions = self.analyze_commuting_costs()
     commuting_step = DecarbStep(
       step_type=DecarbStepType.COMMUTING_INDIVIDUAL,
          cur_cost=commuting_costs,
          new_cost=self.commuting_analyzer.stipent_individual(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location, 1, 50, 2,30)[2],
         cur_emissions=commuting_emissions,
          new_emissions=commuting_emissions * 0.9,  # fake num
           description="Analyze commuting costs and emissions for individual",
           difficulty=1, transition_percentage=25
       )
     self.steps.append(commuting_step)
    
    def run_carpool_step(self):
       # commuting cost for carpool
        commuting_costs, commuting_emissions = self.analyze_commuting_costs()
        carpool_savings,carpool_saving_emission = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,2,30)
        commute_steps = self.commuting_analyzer.carpool_savings_details(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,2,30)
        print(f'init commuting_costs is {commuting_costs}')
        print(f'init commuting_emi is {commuting_emissions}')
        print(f'init carpool commuting savings is {carpool_savings}')
        print(f'new carpool commuting savings is {carpool_saving_emission}')

        commuting_step = DecarbCommuteStep(
        step_type=DecarbStepType.COMMUTING_CARPOOL,
        cur_cost=commuting_costs,
        new_cost = commuting_costs-carpool_savings,
        new_emissions = carpool_saving_emission,
        cur_emissions=commuting_emissions,
        description="Analyze commuting costs and emissions for carpool", 
        difficulty= 3,transition_percentage=25,commute_steps=commute_steps
     )
        self.steps.append(commuting_step)

    def init_flight_analyzer(self, origin, destination, departure_date, return_date):
        self.flight_analyzer = FlightDataAnalyzer(self.FLIGHT_API_KEY,self.weights, origin, destination, departure_date, return_date)

    def run_flight_step(self, origin, destination, departure_date, return_date):
        self.init_flight_analyzer(origin, destination, departure_date, return_date)

        #flight costs
        optimal_flight = self.flight_analyzer.analyze_flight_costs()
        flight_step = self.create_flight_step(optimal_flight, 3)
        self.steps.append(flight_step)

    def run_return_flight_step(self):
        # Assumes that run_flight_step has been called first.
        return_flight = self.flight_analyzer.get_return_flight_options()
        return_flight_step = self.create_flight_step(return_flight, 3)
        self.steps.append(return_flight_step)
    def run_CRU_step(self):
        # CRU Step
        cru_step = self.create_CRU_step()
        cru_step.recommendations =  self.provide_cru_recommendations(cru_step)
        print(cru_step.recommendations)
        self.steps.append(cru_step)
        
    def provide_recommendations(self, electric_step):
       now = datetime.datetime.now()
       current_year = now.year
    
       month = now.month
       current_quarter = (month - 1) // 3 + 1
       electric_recs = Electric_Recommendations(self.provider_info, electric_step,current_year,current_quarter,electric_step.new_cost)
       return electric_recs.to_dict()
    
    def provide_cru_recommendations(self, cru_step):
       now = datetime.datetime.now()
       current_year = now.year
       cru_recs = CRU_Recommendations(self.provider_info, cru_step,current_year,4,cru_step.new_cost)
       return cru_recs.to_dict()

    def run_electric_step(self): 
        # Electricity Step
        electric_step = self.test_electric_lcu_cca(0.5,0.5)
        electric_step.recommendations = self.provide_recommendations(electric_step)
        self.steps.append(electric_step)

        return self.steps

    def get_step_savings(self):
        savings = 0
        for step in self.steps:
            savings += step.compute_emissions_savings()
        return savings
    
    def run_decarb_engine(self):
        self.run_commuting_step()
        self.run_carpool_step()
        self.run_electric_step()
        self.run_flight_optimizer_step()
        self.run_CRU_step()

        return self.steps
    
    def run_flight_analyzer(decarb_engine):
        origin = "LAX"
        destination = "JFK"
        departure_date = "2025-01-30"
        return_date = "2025-01-31"
        decarb_engine.run_flight_step(origin, destination, departure_date, return_date)
        decarb_engine.run_return_flight_step()

    def create_flight_step(self, return_flight, difficulty):
        return_flight_savings = return_flight['Price'].iloc[0]
        return_flight_emissions = return_flight['Carbon Emissions'].iloc[0]
        return_flight_step = FlightDecarbStep(
            cur_cost=self.pre_flight_cost, 
            new_cost=return_flight_savings,
            cur_emissions=return_flight_emissions * 1.1, # fake
            new_emissions=return_flight_emissions,
            description="Analyze flight costs and emissions",
            num_stops=return_flight['Stops'].iloc[0],
            difficulty=difficulty,
            transition_percentage=50
        )
        return return_flight_step
    
    def create_commuting_test_df():
        return pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'method':['car','car','car', 'car','car','car', 'car','uber','car', 'car'],
            'locations':['1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ','3006 San Pablo Ave, Berkeley, CA ' ],
            'frequency': [22, 20, 18, 22, 20, 18, 22, 20, 18, 20],
            'cost_per_km':[0.1,0.2,0.3, 0.1,0.2,0.3, 0.1,0.2,0.3, .4]
        })
    
    def create_dynamic_test_df():
        return pd.DataFrame({
            'method': ['bus', 'train', 'uber'],
            'distance': [10, 10, 10],
            'cost_per_km': [0.1, 0.2, 0.7]
        })

    def test_decarb_engine():
        firm = '2107 Addison St, Berkeley, CA'
        
        commuting_data = DecarbEngine.create_commuting_test_df()
        df_dynamic = DecarbEngine.create_dynamic_test_df()
        weights = DecarbWeight(0.4, 0.3, 0.2, 0.1) 
        prev_cost = 800
        decarb_goals = DecarbEngine.create_customer_decarb_goals()
        decarb_engine = DecarbEngine(commuting_data, df_dynamic,firm, weights,prev_cost, decarb_goals)
        decarb_engine.run_electric_tests()
        decarb_engine.run_flight_analyzer()
        
    def create_customer_decarb_goals():
        customer_id = 10 
        year = 2025
        scope1_emissions = 1000 
        scope2_emissions = 1500.5 
        scope3_emissions= 5000.2 
        scope1_target = .55 
        scope2_target = .75 
        scope3_target = .25
        time_frame = 5
        decarb_goals = DecarbCustomerGoals(time_frame,customer_id, year, scope1_emissions, scope2_emissions, scope3_emissions, scope1_target, scope2_target, scope3_target)
        return decarb_goals

    def create_decarb_engine():
        firm = '2107 Addison St, Berkeley, CA'
        commuting_data = DecarbEngine.create_commuting_test_df()
        df_dynamic = DecarbEngine.create_dynamic_test_df()
        decarb_goals = DecarbEngine.create_customer_decarb_goals()
        weights =  DecarbWeight(0.4, 0.3, 0.2, 0.1) 
        pre_cost = 800
        decarb_engine = DecarbEngine(commuting_data, df_dynamic, firm, weights,pre_cost, decarb_goals)
        decarb_steps = decarb_engine.run_decarb_engine()
        decarb_engine.run_flight_analyzer()
        decarb_engine.compute_zscore()

        electric_recs = []
        for step in decarb_steps:
            if type(step) is ElectricDecarbStep:
                # Electric_Recommendations
                electric_recs = step.recommendations
                break

        

    def get_cur_quadrant(self):
        x = datetime.datetime.now().month
        return (x - 1) // 3 + 1
    
    # Helper function to handle JSON serialization
    def convert_to_json_serializable(self, data):
        if isinstance(data, dict):
            return {key: self.convert_to_json_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_json_serializable(item) for item in data]
        elif isinstance(data, np.integer):
            return int(data)
        elif isinstance(data, np.floating):
            return float(data)
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, ProviderInfo):
            return data.to_dict()
        elif isinstance(data, ProviderInfoCru):
            return data.to_dict()
        elif isinstance(data, set):
            return list(data)
        elif isinstance(data, pd.DataFrame):
        # Convert DataFrame to a list of dictionaries (JSON serializable format)
            return data.to_dict(orient='records')
        else:
            return data
        
    def query_cs_backend_api(self,company_id):
        """
    This function makes an API request to the CS backend API to fetch carbon emission data.
    For now, it returns a hardcoded JSON response.
        """
    #URL
    #api_url = f"create API"

    # response = requests.get(api_url)
    # json_data = response.json()

    #Hardcoded data for now
        json_data = {
            "company_id": company_id,
            "current_details":{
              "current_provider":"ABC",
              "current_plan":"PLAN-A",
              "current_cost":2000,
              "current_emissions":20000
            },
            "scope_total": {
            "scope_1_total": 100,
            "scope_2_total": 50,
            "scope_3_total": 10,
            "scope_total": 160,
            "scope_1_target": 0.75,
            "scope_2_target": 1.0,
            "scope_3_target": 0.50,
            "target_timeframe": 5
        }
    }

        return json_data
        
    def create_decarb_engine_with_yearly_goals(decarb_goals, output_file='yearly_quarterly_steps.json'):
    # Step 1: Initialize the decarbonization engine
     firm = '2107 Addison St, Berkeley, CA'
     commuting_data = DecarbEngine.create_commuting_test_df()
     df_dynamic = DecarbEngine.create_dynamic_test_df()
     
     weights = DecarbWeight(0.4, 0.3, 0.2, 0.1)
     pre_cost = 800
     decarb_engine = DecarbEngine(commuting_data, df_dynamic, firm, weights, pre_cost, decarb_goals)
     decarb_steps = decarb_engine.run_decarb_engine()
     decarb_engine.run_flight_analyzer()
     dict_zscore = decarb_engine.get_dict_zscore(decarb_steps)
     print("DECARB",decarb_steps)
     #data such as facilities--> For calcualtion of transition percentage
     current_quarter = decarb_engine.get_cur_quadrant() 
     current_year = int(decarb_goals.year)
     yearly_steps_orig = decarb_engine.init_yearly_steps(decarb_goals.customer_id,decarb_goals.timeframe, current_year, current_quarter)
     
     yearly_steps=[]

     electric_step = None
     cru_step=None
     flight_optimizer= None
     flight_step=None
     
     commute_step=None
     for goal_yr in range(decarb_goals.timeframe):
      cur_goal_yr = current_year + goal_yr
      cur_goal_quarter = current_quarter

      for quarter in range(1, 5):  # Iterate through all four quarters
        for quarter_step in yearly_steps_orig:
            if quarter_step.year == cur_goal_yr and quarter_step.quarter == quarter:
                # Add steps to the corresponding quarter
                for step in decarb_steps:
                    if isinstance(step, ElectricDecarbStep):
                            electric_step = step  
                    else:
                            quarter_step.add_step(step)                               
                
                # Append quarter_step if it's not already in yearly_steps
                if quarter_step not in yearly_steps:
                    yearly_steps.append(quarter_step)
        
        # Update current quarter for the next iteration
        cur_goal_quarter = (cur_goal_quarter % 4) + 1
      for quarter_step in yearly_steps_orig:
             if quarter_step.year == cur_goal_yr and quarter_step.quarter == 4:
                for step in decarb_steps:
                    if isinstance(step, CRUDecarbStep):
                        cru_step = step
                    elif isinstance(step,FlightDecarbStep):
                        flight_step=step
                    elif isinstance(step,FlightOptimizerDecarbStep):
                        flight_optimizer=step
                    elif isinstance(step,DecarbCommuteStep):
                        commute_step=step
                    else: 
                        quarter_step.add_step(step)

                if quarter_step not in yearly_steps:
                    yearly_steps.append(quarter_step)
      
     # Add Electric Steps as Quarter Steps, once per Year
     cur_e_year = current_year
     for goal_yr in range(decarb_goals.timeframe):
      
        cur_e_year =current_year+goal_yr
        print(goal_yr)
        e_rec = electric_step.recommendations['recommendations'][goal_yr]
        cru_rec=cru_step.recommendations
        for quarter_step in yearly_steps_orig:
            if quarter_step.year == cur_e_year and quarter_step.quarter == current_quarter:
              print("Adding the electric rec once a year")
              print(e_rec)
              quarter_step.add_electric_step(e_rec, electric_step) 
        for quarter_step in yearly_steps_orig:
            if quarter_step.year == cur_e_year and quarter_step.quarter == 3:
              print("Adding the optimiser rec once a year")
              print(flight_optimizer)
              print("commute",commute_step)
              quarter_step.add_flight_step(flight_step)
              quarter_step.add_flight_step(flight_optimizer)  
              quarter_step.add_commute_step(commute_step)
              
        for quarter_step in yearly_steps_orig:
            if quarter_step.year == cur_e_year and quarter_step.quarter == 4:
              print("Adding the CRU rec once a year")
              print(cru_step)
              quarter_step.add_cru_step(cru_rec,cru_step)  
          
    # Step 5: Ensure CRU is only purchased once a year
     decarb_engine.add_cru_steps(yearly_steps)
     output_data=decarb_engine.query_cs_backend_api(10)

     data=decarb_engine.output_json_to_file(output_data,yearly_steps, output_file)
     load_json_data(data,output_data)
     

    

    def init_yearly_steps(self, company_id,timeframe, current_year, current_quarter):
     # Step 3: Create quarterly goals
     yearly_steps = []
     cur_quarter = current_quarter
     cur_year=current_year
     for _ in range(timeframe):
        while cur_quarter < 5:  
            # Initialize a QuaterStep instance
            quarter_step = QuarterStep(
                company_id=company_id,
                year=cur_year,
                quarter=cur_quarter,
                
            )
            yearly_steps.append(quarter_step)
            cur_quarter+=1
        
        cur_quarter=1
        cur_year+=1
        if(cur_year==current_year+timeframe):
            break
     return yearly_steps
     
    
    def add_cru_steps(self, yearly_steps):
        print(" ")
        # cru_purchased = False
        # for quarter_step in yearly_steps:
        #     if not cru_purchased:
        #         if any("CRU" in step.description for step in quarter_step.scope1_steps + quarter_step.scope2_steps + quarter_step.scope3_steps):
        #             cru_purchased = True
        #     else:
        #         quarter_step.scope1_steps = [step for step in quarter_step.scope1_steps if "CRU" not in step.description]
        #         quarter_step.scope2_steps = [step for step in quarter_step.scope2_steps if "CRU" not in step.description]
        #         quarter_step.scope3_steps = [step for step in quarter_step.scope3_steps if "CRU" not in step.description]
        
    def get_dict_zscore(self, decarb_steps):
        (f"decarb_steps length {len(decarb_steps)}")
        [(f"step {step}") for step in decarb_steps]
    
        # Step 2: Compute difficulties, savings, and emissions
        difficulties = [float(step.difficulty) for step in decarb_steps]
        savings = [float(step.compute_savings()) for step in decarb_steps]
        emissions = [float(step.compute_emissions_savings()) for step in decarb_steps]

        mean_diff = float(np.mean(difficulties))
        mean_savings = float(np.mean(savings))
        mean_emissions = float(np.mean(emissions))

        std_diff = float(np.std(difficulties))
        std_savings = float(np.std(savings))
        std_emissions = float(np.std(emissions))

        total_savings = 0
        total_emission_savings = 0
        total_zscore = 0
    
        dict_zscore = {}
        for step in decarb_steps:
            this_savings = step.compute_savings()
            this_emission_savings = step.compute_emissions_savings()
            total_savings += this_savings
            total_emission_savings += this_emission_savings

            this_z_score = step.compute_ranking_zscore(mean_diff, std_diff, mean_savings, std_savings, mean_emissions, std_emissions)
            total_zscore += this_z_score

            this_step_type = step.step_type.name
            dict_zscore[this_step_type] = this_z_score

           

        num_steps = len(decarb_steps)
        dict_zscore["avg-zscore"] = total_zscore / num_steps if num_steps > 0 else 0
        return dict_zscore


    def output_json_to_file(self, output_data,yearly_steps_array, output_file):
        company_id = output_data["company_id"]
         # Convert data to JSON-serializable format
        company_id = output_data["company_id"]
        json_data = [quarter_step.to_dict(company_id) for quarter_step in yearly_steps_array]
        json_data_serializable = self.convert_to_json_serializable(json_data)  
        output_data = {
        "cs_backend_data": output_data,
        "yearly_steps": json_data_serializable
         }
        # Save the result as a JSON file
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)

        print(json_data_serializable)

        return json_data_serializable

    def create_CRU_step(self):
        initial_per = 0.1
        initial_cost = 22.5
        emission = 20000
        CRU_amt = initial_per*emission
        cost = initial_cost*CRU_amt
        CRU_step = Decarb_CRU(
            cur_cost=0, 
            new_cost=cost,
            cur_emissions=emission, # fake
            new_emissions=emission-CRU_amt,
            CRU_amount=1000, #for testing
            description="Analyze CRU costs and emissions",
            difficulty=1,
            timeframe=5,
            transition_percentage=35
        )
        return CRU_step

    def plan_reduction(self,current_emissions, reduction_target, timeframe):
        # Calculate the target emissions
        target_emissions = current_emissions * (1 - reduction_target / 100)
        annual_reduction = (current_emissions - target_emissions) / timeframe

        # Generate a reduction plan
        plan = []
        for year in range(1, timeframe + 1):
            year_emissions = current_emissions - (annual_reduction * year)
            plan.append({
                'year': year,
                'target_emissions': year_emissions
            })

        return plan

    def display_reduction_plan(self, plan):
        for step in plan:
            print(f"Year {step['year']}: Target Emissions = {step['target_emissions']} metric tons")
        #sorted_zscores = sorted(dict_zscore.items(), key=lambda item: item[1], reverse=True)
            
    def run_flight_optimizer_step(self):
     flights_user = [
        Flight(
            non_stop=True,
            flight_class="Economy",
            airplane_model="Boeing 737-400",
            departure_airport="JFK",
            arrival_airport="LAX",
            cost=200
        ),
        Flight(
            non_stop=False,
            flight_class=None,
            airplane_model=None,
            departure_airport="SFO",
            arrival_airport="JFK",
            cost=500,
            stops=[Flight(
                non_stop=True,
                flight_class="Economy",
                airplane_model="Airbus A320",
                departure_airport="SFO",
                arrival_airport="LAX",
                cost=250
            ),Flight(
                non_stop=True,
                flight_class="Economy",
                airplane_model="Boeing 737-400",
                departure_airport="LAX",
                arrival_airport="JFK",
                cost=250
            )]
        ),
        Flight(
            non_stop=False,
            flight_class=None,
            airplane_model=None,
            departure_airport="OKC",
            arrival_airport="DCA",
            cost=1000,
            stops=[Flight(
                non_stop=True,
                flight_class="Business",
                airplane_model="Airbus A320",
                departure_airport="OKC",
                arrival_airport="DFW",
                cost=500
            ),Flight(
                non_stop=True,
                flight_class="Premium Economy",
                airplane_model="Boeing 737-400",
                departure_airport="DFW",
                arrival_airport="DCA",
                cost=500
            )]
        )
    ]
     cur_total_emissions=0
     new_total_emissions=0
     cur_total_cost=0
     new_total_cost=0
     for flight in flights_user:
         cur_total_cost += flight.cost
         new_total_cost += flight.cost
         original_distance,cur_emissions,optimized_flight=self.emissions_df.find_optimized_flight(flight)
         cur_total_emissions+=cur_emissions
         new_total_emissions+=optimized_flight['emissions']
         if original_distance is None:
             raise ValueError (f"Wrong airport code{flight.departure_airport},{flight.arrival_airport}")
    
         cur_total_emissions = round(cur_total_emissions, 2)
         new_total_emissions = round(new_total_emissions, 2)

     description="Reduction in emissions of flights"
     difficulty=5
     transition_percentage=0
     decarb_step=FlightOptimizerDecarbStep(cur_total_cost,new_total_cost, cur_total_emissions, new_total_emissions, description, difficulty,transition_percentage,num_stops=2)
     
     self.steps.append(decarb_step)
     print(self.steps)
    
    ######
    # Test Code
    ######
    
    def run_electric_tests(self):
        cost_optimise=1
        carbon_optimise=0
        #cost_optimise=0.5
        #carbon_optimise=0.5
        #cost_optimise=0
        #carbon_optimise=1
    
        self.test_electric_lcb_cca(cost_optimise, carbon_optimise)
        self.test_electric_lcu_cca(cost_optimise, carbon_optimise)
        self.test_electric_smb_cca(cost_optimise, carbon_optimise)
        self.test_electric_smu_cca(cost_optimise, carbon_optimise)
        self.test_electric_lcb(cost_optimise, carbon_optimise)
        self.test_electric_lcu(cost_optimise, carbon_optimise)
        self.test_electric_smb(cost_optimise, carbon_optimise)
        self.test_electric_smu(cost_optimise, carbon_optimise)

    def test_electric_lcu_cca(self, cost_optimise, carbon_optimise):
        print("test_electric_lcu_cca")
        user_zip_code = 94706
        user_bundled = 'No'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-19_SV'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        self.provider_info='PG&E'
        self.new_provider_info='None'

        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcu",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
        
    def test_electric_smb_cca(self, cost_optimise, carbon_optimise):
        print("test_electric_smb_cca")
        user_zip_code = 94706
        user_bundled = 'Yes'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-10_S'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        self.provider_info='Ava Bright Choice'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smb",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
    
    def test_electric_smu_cca(self, cost_optimise, carbon_optimise):
        print("test_electric_smu_cca")
        user_zip_code = 94706
        user_bundled = 'No'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-10_S'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        self.provider_info='Ava Bright Choice'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smu",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
    
    def test_electric_lcb_cca(self, cost_optimise, carbon_optimise):
        print("test_electric_lcb_cca")
        user_zip_code = 94706
        user_bundled = 'Yes'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-19_SV'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        self.provider_info='Ava Bright Choice'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcb",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
    
    def test_electric_lcb(self, cost_optimise, carbon_optimise):
        print("test_electric_lcb")
        user_zip_code = 95948
        user_bundled = 'Yes'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-20_TV'
        UseCCA = 'No'
        HasCCA = 'No'
        self.provider_info='PG&E'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcb",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
    
    def test_electric_lcu(self, cost_optimise, carbon_optimise):
        print("test_electric_lcu")
        user_zip_code = 95948
        user_bundled = 'No'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-19_TV'
        UseCCA = 'No'
        HasCCA = 'No'
        self.provider_info='PG&E'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcu",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
    
    def test_electric_smb(self, cost_optimise, carbon_optimise):
        print("test_electric_smb")
        user_zip_code = 95948
        user_bundled = 'Yes'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-6'
        UseCCA = 'No'
        HasCCA = 'No'
        self.provider_info='PG&E'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smb",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)
    
    def test_electric_smu(self, cost_optimise, carbon_optimise):
        print("test_electric_smu")
        user_zip_code = 95948
        user_bundled = 'No'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-10_SV'
        UseCCA = 'No'
        HasCCA = 'No'
        self.provider_info='PG&E'
        self.new_provider_info='None'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smu",cost_optimise,carbon_optimise,self.provider_info,self.new_provider_info)

    def test_electric_step(self, user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, usage_type,cost_optimise,carbon_optimise,provider_info,new_provider_info):
        user_input_peak_usage=25
        user_input_part_peak_usage = 25
        user_input_super_off_peak_usage=25
        user_input_off_peak_usage=25
        kwh_used = user_input_peak_usage + user_input_part_peak_usage + user_input_super_off_peak_usage + user_input_off_peak_usage
        meter_input = 7
        time_in_use = 8
        max_15min_usage = 9
        user_cur_cost = 100000
        difficulty = 2
        ranking_zscore = 10
        user_current_company = "PG&E"
        user_electricity_bill_season = "Summer"
        user_B1STB_highest_demand_15mins = 9
        user_B1STU_highest_demand_15mins = 9
        transition_percentage=25
        
        usage_data = None
        if usage_type == "lcb":
            usage_data = self.create_lcb(user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage, user_input_part_peak_usage, user_electricity_bill_season, meter_input,time_in_use,max_15min_usage,user_sector,user_current_plan,kwh_used )
        elif usage_type == "lcu":
            usage_data = self.create_lcu(user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage, user_input_part_peak_usage, user_electricity_bill_season, meter_input,time_in_use,max_15min_usage,user_sector,user_current_plan,kwh_used)
        elif usage_type == "smu":
            usage_data = self.create_smu(user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage, user_input_part_peak_usage, meter_input,time_in_use,max_15min_usage,user_sector,user_B1STU_highest_demand_15mins,kwh_used)
        elif usage_type == "smb":
            usage_data = self.create_smb(user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage, user_input_part_peak_usage, meter_input,time_in_use,max_15min_usage,user_sector,user_B1STB_highest_demand_15mins,kwh_used)
        
        electric_step = ElectricDecarbStep(user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled, user_current_company, 
                                user_current_plan, UseCCA, HasCCA, usage_data, ranking_zscore, difficulty,transition_percentage,meter_input, time_in_use, max_15min_usage,cost_optimise,carbon_optimise,provider_info,new_provider_info) 
        
        return electric_step
    
    #(20,20,20,20,'Summer',7,8,9,'Large Commercial and Industrial','B-19_TV')
    def create_lcb(self, user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage,user_input_part_peak_usage, user_electricity_bill_season, meter_input,time_in_use,max_15min_usage, user_sector,user_current_plan,kwh_used):
        lcb_usage_data = LCBSector_simplified(user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage, user_electricity_bill_season, meter_input,time_in_use,max_15min_usage, user_sector,user_current_plan,kwh_used)
        return lcb_usage_data
    
    #20, 20, 20, 20, 7, 8, 9, 'Small and Medium Business',2
    def create_smb(self, user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage,user_input_part_peak_usage, meter_input,time_in_use,max_15min_usage, user_sector,user_B1STB_highest_demand_15mins,kwh_used):
        smb_usage_data = SMBSector_simplified(user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage,meter_input,time_in_use,max_15min_usage, user_sector,user_B1STB_highest_demand_15mins,kwh_used)
        smb_usage_data.update()
        return smb_usage_data
    
    #20,20,20,20,'Summer',7,8,9,'Large Commercial and Industrial','B-19_TV'
    def create_lcu(self, user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage,user_input_part_peak_usage, user_electricity_bill_season, meter_input,time_in_use,max_15min_usage, user_sector,user_current_plan,kwh_used):
        lcu_usage_data = LCUSector_simplified(user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage, user_electricity_bill_season, meter_input,time_in_use,max_15min_usage, user_sector,user_current_plan,kwh_used)
        return lcu_usage_data
    
    #20, 20, 20, 20, 7, 8, 9, 'Small and Medium Business',2
    def create_smu(self, user_input_peak_usage, user_input_off_peak_usage, user_input_super_off_peak_usage,user_input_part_peak_usage, meter_input,time_in_use,max_15min_usage, user_sector,user_B1STU_highest_demand_15mins,kwh_used):
        smu_usage_data = SMUSector_simplified(user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage,meter_input,time_in_use,max_15min_usage, user_sector,user_B1STU_highest_demand_15mins,kwh_used)
        smu_usage_data.update()
        return smu_usage_data
    
def main():
    #DecarbEngine.create_decarb_engine()
    decarb_goals = DecarbEngine.create_customer_decarb_goals()
    DecarbEngine.create_decarb_engine_with_yearly_goals(decarb_goals)
    #DecarbEngine.test_decarb_engine()
    
 
if __name__ == "__main__":
    main()
    
    
# -*- coding: utf-8 -*-
"""DecarbEngine.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EWIicIg05wODK4aX-Dk-DY5WdoQz968r
"""
import numpy as np
from components.biz_commute_analyzer import BusinessCommutingAnalyzer
from steps.electric_decarb_step import ElectricDecarbStep
from components.electricity.sectors.lcbsector import LCBSector_simplified
from components.electricity.sectors.lcusector import LCUSector_simplified
from components.electricity.sectors.smbsector import SMBSector_simplified
from components.electricity.sectors.smusector import SMUSector_simplified
from components.flight_data_analyzer import FlightDataAnalyzer
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType
from steps.decarb_weight import DecarbWeight
import pandas as pd
from steps.flight_decarb_step import FlightDecarbStep
from components.FlightEmissionsCalculator import FlightEmissionsCalculator
from components.FlightEmissionsCalculator import Flight
from steps.decarb_emissions_step import EmissionsDecarbStep

class DecarbEngine:
    def __init__(self, commuting_data,dynamic_data, origin, destination, departure_date,firm,weights,pre_flight_cost,return_date=None):
        self.GOOGLE_MAPS_API_KEY = "AIzaSyD1fbsNKLIWwHly5YcSBcuMWhYd2kTIN08"
        self.FLIGHT_API_KEY = '3d9d866dbc47001e268d6b82890721368c0a0d1a9fd4d9ca8eaf4f5e4a8c5d23'
        self.OIL_PRICE_API_KEY = 'jDLAcmPbuXd1CMXRjKFZMliukSgC6ujhUjnKaxOf'
        self.COORDINATES_API_KEY = "0c608aea6eb74a9da052e7a83df8c693"
        self.firm = firm
        self.dynamic = dynamic_data
        self.weights = weights
        self.pre_flight_cost = pre_flight_cost
        self.emissions_df = FlightEmissionsCalculator("Emissions_Flights.xlsx", self.COORDINATES_API_KEY)

        self.commuting_analyzer = BusinessCommutingAnalyzer(commuting_data, self.GOOGLE_MAPS_API_KEY, self.OIL_PRICE_API_KEY,self.firm,self.dynamic)
        self.flight_analyzer = FlightDataAnalyzer(self.FLIGHT_API_KEY,self.weights, origin, destination, departure_date, return_date)
        self.steps = []
    
    def plan_emissions_reduction(self, current_emissions, reduction_targets, timeframe, actions):
      
       
        target_emissions = {
            scope: current_emissions[scope] * (1 - reduction_targets[scope] / 100)
            for scope in current_emissions
        }
        annual_reduction = {
            scope: (current_emissions[scope] - target_emissions[scope]) / timeframe
            for scope in current_emissions
        }

        plan = []
        for year in range(1, timeframe + 1):
            year_plan = {
                'year': year,
                'target_emissions': {
                    scope: current_emissions[scope] - (annual_reduction[scope] * year)
                    for scope in current_emissions
                },
                'actions': {
                    'Scope 1': [],
                    'Scope 2': [],
                    'Scope 3': []
                }
            }
            for action in actions:
                scope = action.get('scope', 'Scope 3')  
                action_impact = annual_reduction[scope] / len([a for a in actions if a['scope'] == scope])  
                year_plan['actions'][scope].append({
                    'action': action['name'],
                    'impact': action_impact
                })
            plan.append(year_plan)

        return plan
    def display_emissions_reduction_plan(self, plan):
        """
        Display the emissions reduction plan.

        :param plan: The emissions reduction plan to display.
        """
        for step in plan:
            print(f"Year {step['year']}:")
            for scope in ['Scope 1', 'Scope 2', 'Scope 3']:
                target_emissions = step['target_emissions'][scope]
                print(f"  {scope}: Target Emissions = {target_emissions} metric tons")
                for action in step['actions'][scope]:
                    print(f"    Action: {action['action']} - Impact: {action['impact']} metric tons")



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
            difficulty=1
        )
        self.steps.append(commuting_step)
    #def CRU(self):

    
    def run_carpool_step(self):
        # commuting cost for carpool
        commuting_costs, commuting_emissions = self.analyze_commuting_costs()
        carpool_savings,carpool_saving_emission = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,2,30)
        print(f'init commuting_costs is {commuting_costs}')
        print(f'init commuting_emi is {commuting_emissions}')
        print(f'init carpool commuting savings is {carpool_savings}')

        print(f'new carpool commuting savings is {carpool_saving_emission}')

     

        



        

        commuting_step = DecarbStep(
            step_type=DecarbStepType.COMMUTING_CARPOOL,
            cur_cost=commuting_costs,
            new_cost = commuting_costs-carpool_savings,
            new_emissions = carpool_saving_emission,
            cur_emissions=commuting_emissions,
            description="Analyze commuting costs and emissions for carpool", 
            difficulty= 3
        )
        
        self.steps.append(commuting_step)

    def run_flight_step(self):
        #flight costs
        optimal_flight = self.analyze_flight_costs()
        #print(optimal_flight)
        flight_step = self.create_flight_step(optimal_flight, 3)
        self.steps.append(flight_step)

    def run_return_flight_step(self):
        # return flight
        return_flight = self.get_return_flight_options()
        return_flight_step = self.create_flight_step(return_flight, 3)
        self.steps.append(return_flight_step)
        
    def run_electric_step(self):
        # Electricity Step
        electric_step = self.test_electric_smu()
        self.steps.append(electric_step)

    def get_step_savings(self):
        savings = 0
        for step in self.steps:
            savings += step.compute_emissions_savings()
        return savings
    


    def run_decarb_engine(self):
        #self.run_commuting_step()
        #self.run_carpool_step()
        self.run_flight_step()
        self.run_return_flight_step()
        #self.run_electric_step()
        #self.create_user_flight_step()

        return self.steps
        
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
            difficulty=difficulty
        )
        return return_flight_step
    
    def test_decarb_engine():
        origin = "LAX"
        destination = "JFK"
        departure_date = "2024-08-20"
        return_date = "2024-08-24"
        firm = '2107 Addison St, Berkeley, CA'
        commuting_data = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'method':['car','car','car', 'car','car','car', 'car','uber','car', 'car'],
            'locations':['1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ','3006 San Pablo Ave, Berkeley, CA ' ],
            'frequency': [22, 20, 18, 22, 20, 18, 22, 20, 18, 20],
            'cost_per_km':[0.1,0.2,0.3, 0.1,0.2,0.3, 0.1,0.2,0.3, .4]
        })

        df_dynamic = pd.DataFrame({
            'method': ['bus', 'train', 'uber'],
            'distance': [10, 10, 10],
            'cost_per_km': [0.1, 0.2, 0.7]
        })

        weights =  DecarbWeight(0.4, 0.3, 0.2, 0.1) 
        prev_cost = 800
        decarb_engine = DecarbEngine(commuting_data, df_dynamic,origin, destination, departure_date, firm, weights,prev_cost,return_date)
        decarb_engine.run_tests()

    def create_decarb_engine():
        origin = "LAX"
        destination = "JFK"
        departure_date = "2024-08-11"
        return_date = "2024-08-13"
        firm = '2107 Addison St, Berkeley, CA'
        commuting_data = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'method':['car','uber','car', 'car','uber','car', 'car','uber','car', 'car'],
            'locations':['1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ','3006 San Pablo Ave, Berkeley, CA ' ],
            'frequency': [22, 20, 18, 22, 20, 18, 22, 20, 18, 20],
            'cost_per_km':[0.1,0.2,0.3, 0.1,0.2,0.3, 0.1,0.2,0.3, .4]
        })

        df_dynamic = pd.DataFrame({
            'method': ['bus', 'train', 'uber'],
            'distance': [10, 10, 10],
            'cost_per_km': [0.1, 0.2, 0.7]
        })

        weights =  DecarbWeight(0.4, 0.3, 0.2, 0.1) 
        pre_cost = 800
        decarb_engine = DecarbEngine(commuting_data, df_dynamic,origin, destination, departure_date, firm, weights,pre_cost,return_date)
        decarb_steps = decarb_engine.run_decarb_engine()
        
        difficulties = [step.difficulty for step in decarb_steps]
        savings = [step.compute_savings() for step in decarb_steps]
        combined_series = pd.concat(savings[:2])

# Append the integers to the combined Series
        combined_list = combined_series.tolist() + savings[2:]

# Compute the mean
        mean_value = sum(combined_list) / len(combined_list)

        #print("Mean value:", mean_value)

        emissions = [step.compute_emissions_savings() for step in decarb_steps]

        mean_diff = np.mean(difficulties)
        std_diff = np.std(difficulties)

        mean_savings = mean_value
        std_savings = np.std(combined_list)
        mean_emissions = np.mean(emissions)
        std_emissions = np.std(emissions)

        total_savings = 0
        total_emission_savings = 0
        dict_zscore = {}
        for step in decarb_steps:
            this_savings = np.mean(step.compute_savings())
            this_emission_savings = step.compute_emissions_savings()
            total_savings += this_savings
            total_emission_savings += this_emission_savings

            dict_zscore[step.step_type] = np.mean(step.compute_zscore(mean_diff, std_diff, mean_savings, std_savings, mean_emissions, std_emissions))
            
            print(step.generate_step_description())
            print(f"z-score is: {dict_zscore[step.step_type]}")
            print(f"Difficulty: {step.difficulty}")  
            print(f"Savings: ${np.mean(this_savings)}")
            print(f"Emissions Savings: {this_emission_savings} kg CO2\n")
        #print(dict_zscore)
        print(f"Total Savings: ${total_savings}")
        print(f"Total Emissions Savings: {total_emission_savings} kg CO2\n")
        
        #print(dict_zscore)
        #global_emission = 
        
        
    def CRU():
        initial_per = 0.1
        initial_cost = 22.5
        emission = DecarbEngine.create_decarb_engine()
        CRU_amt = initial_per*emission
        cost = initial_cost*CRU_amt
        leftover = emission-CRU_amt
        return cost,leftover


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
    def create_user_flight_step(self):
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
            stops=[
                {
                    "departure_airport": "SFO",
                    "arrival_airport": "LAX",
                    "airplane_model": "Airbus A320",
                    "class": "Economy"
                },
                {
                    "departure_airport": "LAX",
                    "arrival_airport": "JFK",
                    "airplane_model": "Boeing 737-400",
                    "class": "Economy"
                }
            ]
        ),
        Flight(
            non_stop=False,
            flight_class=None,
            airplane_model=None,
            departure_airport="OKC",
            arrival_airport="DCA",
            cost=1000,
            stops=[
                {
                    "departure_airport": "OKC",
                    "arrival_airport": "DFW",
                    "airplane_model": "Airbus A320",
                    "class": "Business"
                },
                {
                    "departure_airport": "DFW",
                    "arrival_airport": "DCA",
                    "airplane_model": "Boeing 737-400",
                    "class": "Premium Economy"
                }
            ]
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
         print("Optimized flight configuration:")
         print(f"Airplane model: {optimized_flight['airplane_model']}")
         print(f"Class: {optimized_flight['class']}")
         print(f"Optimized distance: {optimized_flight['distance']:.2f} miles")
         print(f"Optimized carbon emissions: {optimized_flight['emissions']:.2f} kg")

     description="Reduction in emissions of flights"
     difficulty=5
     decarb_step=EmissionsDecarbStep(cur_total_cost,new_total_cost, cur_total_emissions, new_total_emissions, description, difficulty)
     
     self.steps.append(decarb_step)
    
    
    ######
    # Test Code
    ######
    
    def run_tests(self):
        self.test_electric_lcb_cca()
        self.test_electric_lcu_cca()
        self.test_electric_smb_cca()
        self.test_electric_smu_cca()
        self.test_electric_lcb()
        self.test_electric_lcu()
        self.test_electric_smb()
        self.test_electric_smu()

    def test_electric_lcu_cca(self):
        print("test_electric_lcu_cca")
        user_zip_code = 94706
        user_bundled = 'No'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-19_SV'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcu")
    
    def test_electric_smb_cca(self):
        print("test_electric_smb_cca")
        user_zip_code = 94706
        user_bundled = 'Yes'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-10_S'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smb")
    
    def test_electric_smu_cca(self):
        print("test_electric_smu_cca")
        user_zip_code = 94706
        user_bundled = 'No'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-10_S'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smu")
    
    def test_electric_lcb_cca(self):
        print("test_electric_lcb_cca")
        user_zip_code = 94706
        user_bundled = 'Yes'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-19_SV'
        UseCCA = 'Yes'
        HasCCA = 'Yes'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcb")
    
    def test_electric_lcb(self):
        print("test_electric_lcb")
        user_zip_code = 95948
        user_bundled = 'Yes'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-20_TV'
        UseCCA = 'No'
        HasCCA = 'No'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcb")
    
    def test_electric_lcu(self):
        print("test_electric_lcu")
        user_zip_code = 95948
        user_bundled = 'No'
        user_sector =  'Large Commercial and Industrial'
        user_current_plan ='B-19_TV'
        UseCCA = 'No'
        HasCCA = 'No'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "lcu")
    
    def test_electric_smb(self):
        print("test_electric_smb")
        user_zip_code = 95948
        user_bundled = 'Yes'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-6'
        UseCCA = 'No'
        HasCCA = 'No'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smb")
    
    def test_electric_smu(self):
        print("test_electric_smu")
        user_zip_code = 95948
        user_bundled = 'No'
        user_sector =  'Small and Medium Business'
        user_current_plan ='B-10_SV'
        UseCCA = 'No'
        HasCCA = 'No'
        return self.test_electric_step(user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, "smu")

    def test_electric_step(self, user_zip_code, user_bundled, user_sector, user_current_plan, UseCCA, HasCCA, usage_type):
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
        user_cost_weight = 0.9
        user_renewable_weight = 0.1 
        user_electricity_bill_season = "Summer"
        user_B1STB_highest_demand_15mins = 9
        user_B1STU_highest_demand_15mins = 9
        
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
                                user_current_plan, user_cost_weight,user_renewable_weight, UseCCA, HasCCA, usage_data, ranking_zscore, difficulty,meter_input, time_in_use, max_15min_usage) 

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
    DecarbEngine.create_decarb_engine()
    origin = "LAX"
    destination = "JFK"
    departure_date = "2024-08-11"
    return_date = "2024-08-13"
    firm = '2107 Addison St, Berkeley, CA'
    commuting_data = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'method':['car','uber','car', 'car','uber','car', 'car','uber','car', 'car'],
        'locations':['1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ', '1122 University Ave, Berkeley, CA','2010 Fifth St, Berkeley, CA','3006 San Pablo Ave, Berkeley, CA ','3006 San Pablo Ave, Berkeley, CA ' ],
        'frequency': [22, 20, 18, 22, 20, 18, 22, 20, 18, 20],
        'cost_per_km':[0.1,0.2,0.3, 0.1,0.2,0.3, 0.1,0.2,0.3, .4]
    })

    df_dynamic = pd.DataFrame({
        'method': ['bus', 'train', 'uber'],
        'distance': [10, 10, 10],
        'cost_per_km': [0.1, 0.2, 0.7]
    })

    weights =  DecarbWeight(0.4, 0.3, 0.2, 0.1) 
    pre_cost = 800
    engine = DecarbEngine(commuting_data, df_dynamic,origin, destination, departure_date, firm, weights,pre_cost,return_date)
    current_emissions = {
        'Scope 1': 400, 
        'Scope 2': 300,
        'Scope 3': 300
    }
    reduction_targets = {
        'Scope 1': 20,  
        'Scope 2': 30,
        'Scope 3': 25
    }
    timeframe = 10  
    actions = [
        {"name": "Increase Energy Efficiency(n/a for now)", "scope": "Scope 1"},
        {"name": "Adopt Renewable Energy(electricity)", "scope": "Scope 2"},
        {"name": "Promote Public Transport+ Carpool", "scope": "Scope 3"}
    ]  

    plan = engine.plan_emissions_reduction(current_emissions, reduction_targets, timeframe, actions)
    engine.display_emissions_reduction_plan(plan)

        
if __name__ == "__main__":

    main()
        

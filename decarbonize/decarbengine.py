# -*- coding: utf-8 -*-
"""DecarbEngine.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EWIicIg05wODK4aX-Dk-DY5WdoQz968r
"""

from components.biz_commute_analyzer import BusinessCommutingAnalyzer
from components.electricity.optimization_calculation.electricity_work import ElectricityWork
from components.electricity.optimization_calculation.lcbelectricityrateplan import LCBElectricityRatePlan
from components.electricity.optimization_calculation.lcuelectricityrateplan import LCUElectricityRatePlan
from components.electricity.optimization_calculation.smuelectricityrateplan import SMUElectricityRatePlan
from components.electricity.optimization_calculation.smbelectricityrateplan import SMBElectricityRatePlan
from components.electricity.current_price_calculation.current_electricity import CurrentElectricity
from components.electricity.current_price_calculation.currentlcbelectricityrateplan import currentLCBElectricityRatePlan
from components.electricity.current_price_calculation.currentsmbelectricityrateplan import currentSMBElectricityRatePlan
from steps.electric_decarb_step import ElectricDecarbStep
from components.electricity.sectors.lcbsector import LCBSector 
from components.electricity.sectors.lcbsector import LCBSector_simplified
from components.electricity.sectors.lcusector import LCUSector
from components.electricity.sectors.lcusector import LCUSector_simplified
from components.electricity.sectors.smbsector import SMBSector_simplified
from components.electricity.sectors.smusector import SMUSector_simplified
from components.flight_data_analyzer import FlightDataAnalyzer
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType
from steps.decarb_weight import DecarbWeight
import pandas as pd
from steps.flight_decarb_step import FlightDecarbStep

class DecarbEngine:
    def __init__(self, commuting_data,dynamic_data, origin, destination, departure_date,firm,weights,pre_flight_cost,return_date=None):
        self.GOOGLE_MAPS_API_KEY = "AIzaSyD1fbsNKLIWwHly5YcSBcuMWhYd2kTIN08"
        self.FLIGHT_API_KEY = 'c539880578adba5b128d0dcab0211b20375f9e54d872eafcf989a8cee98942cb'
        self.OIL_PRICE_API_KEY = 'jDLAcmPbuXd1CMXRjKFZMliukSgC6ujhUjnKaxOf'
        self.firm = firm
        self.dynamic = dynamic_data
        self.weights = weights
        self.pre_flight_cost = pre_flight_cost

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
    
    def run_carpool_step(self):
        # commuting cost for carpool
        commuting_costs, commuting_emissions = self.analyze_commuting_costs()
        commuting_step = DecarbStep(
            step_type=DecarbStepType.COMMUTING_CARPOOL,
            cur_cost=commuting_costs,
            new_cost = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location, [1,2,3], 50,2,30)[0],
            new_emissions = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,[1,2,3], 50,2,30)[2],
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
        #self.run_flight_step()
        #self.run_return_flight_step()
        self.run_electric_step()

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
        departure_date = "2024-07-20"
        return_date = "2024-07-24"
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
        pre_cost = 800
        decarb_engine = DecarbEngine(commuting_data, df_dynamic,origin, destination, departure_date, firm, weights,pre_cost,return_date)
        decarb_steps = decarb_engine.run_decarb_engine()
        
     

        total_savings = 0
        total_emission_savings = 0
        dict_zscore = {}
        for step in decarb_steps:
            this_savings = step.compute_savings()
            this_emission_savings = step.compute_emissions_savings()
            total_savings += this_savings
            total_emission_savings += this_emission_savings

            dict_zscore[step.step_type] = step.compute_mean()
            print(step.generate_step_description())
            print(f"Difficulty: ${step.diffifulty}")  
            print(f"Savings: ${this_savings}")
            print(f"Emissions Savings: {this_emission_savings} kg CO2\n")
        print(f"Total Savings: ${total_savings}")
        print(f"Total Emissions Savings: {total_emission_savings} kg CO2\n")
        # zscore
        return dict_zscore
    




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
        user_input_peak_usage=20
        user_input_part_peak_usage = 20
        user_input_super_off_peak_usage=20
        user_input_off_peak_usage=20
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
    #DecarbEngine.test_decarb_engine()
        
if __name__ == "__main__":
    main()
        

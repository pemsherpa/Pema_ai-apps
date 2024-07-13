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
from components.electricity.sectors.smbsector import SMBSector
from components.electricity.sectors.smusector import SMUSector
from components.flight_data_analyzer import FlightDataAnalyzer
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType
from steps.decarb_weight import DecarbWeight
import pandas as pd
from steps.flight_decarb_step import FlightDecarbStep

class DecarbEngine:
    def __init__(self, commuting_data,dynamic_data, origin, destination, departure_date,firm,weights,return_date=None):
        self.GOOGLE_MAPS_API_KEY = "AIzaSyD1fbsNKLIWwHly5YcSBcuMWhYd2kTIN08"
        self.FLIGHT_API_KEY = '7afef474c061eff1d01477d4a67693a2fdb2821437d63642750002ee4350e901'
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
    
    def run_commuting_step(self):
        # commuting costs and emissions for individual
        commuting_costs, commuting_emissions = self.analyze_commuting_costs()
        commuting_step = DecarbStep(
            step_type=DecarbStepType.COMMUTING,
            cur_cost=commuting_costs,

            new_cost=self.commuting_analyzer.stipent_individual(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location, 1,
                                                                 50, 2,30)[2],
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
            step_type=DecarbStepType.COMMUTING,
            cur_cost=commuting_costs,
            new_cost = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,
                                                                       [1,2,3], 50,2,30)[0],
            new_emissions = self.commuting_analyzer.carpool_savings(self.commuting_analyzer.commuting_data,self.commuting_analyzer.firm_location,
                                                                       [1,2,3], 50,2,30)[2],
            cur_emissions=commuting_emissions,
            description="Analyze commuting costs and emissions for carpool", 
            difficulty= 3
        )
        self.steps.append(commuting_step)

    def run_flight_step(self):
        #flight costs
        optimal_flight = self.analyze_flight_costs()
        flight_step = self.create_flight_step(optimal_flight, 3)
        self.steps.append(flight_step)

    def run_return_flight_step(self):
        # return flight
        return_flight = self.get_return_flight_options()
        return_flight_step = self.create_flight_step(return_flight, 3.5)
        self.steps.append(return_flight_step)
        
    def run_electric_step(self):
        # Electricity Step
        electric_step = self.run_electric()
        self.steps.append(electric_step)

    def get_step_savings(self):
        savings = 0
        for step in self.steps:
            savings += step.compute_emissions_savings()
            print(savings)
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
            cur_cost=return_flight_savings * 1.1, # fake
            new_cost=return_flight_savings,
            cur_emissions=return_flight_emissions * 1.1, # fake
            new_emissions=return_flight_emissions,
            description="Analyze return flight costs and emissions",
            num_stops=return_flight['Stops'].iloc[0],
            difficulty=difficulty
        )
        return return_flight_step

        
    def run_electric(self):
        user_zip_code = 95948 #94002
        user_sector = 'Large Commercial and Industrial' #'Small and Medium Business''Large Commercial and Industrial'
        user_bundled = 'Yes'
        user_current_plan = 'B-19_TV'#'B19TVB'
        kwh_used = 10000
        user_cur_cost = 100000
        difficulty = 2
        ranking_zscore = 10

        user_current_company = "PG&E"
        user_cost_weight = 0.6
        user_renewable_weight = 0.4 

        UseCCA = 'No'
        HasCCA = 'No'

        peak_usage=449
        offpeak_usage=2564 
        super_offpeak_usage=5332 
        peak_cost= .39746
        offpeak_cost= .25523
        super_offpeak_cost=.17651

        lcb_usage_data = self.create_lcb(peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost)
        smb_usage_data = self.create_smb(peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost)
        lcu_usage_data = self.create_lcu(peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost)
        smu_usage_data = self.create_smu(peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost)
        
        electric_step = ElectricDecarbStep(user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled, user_current_company, 
                                user_current_plan, user_cost_weight,user_renewable_weight, UseCCA, HasCCA, lcb_usage_data, smb_usage_data, lcu_usage_data, 
                                smu_usage_data, ranking_zscore, difficulty) 
        return electric_step
        
    def create_lcb(self, peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost,):
        lcb_usage_data = LCBSector_simplified(12,13,14,15,'Summer',7,8,9,'Large Commercial and Industrial','B-19_TV')
        
        return lcb_usage_data
    
    def create_smb(self, peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost):
        smb_usage_data = SMBSector(21, 96, 50, 170, 38, 180, 190, 176, 139, 9, 47, 149, 
                                    64, 113, 169, 159, 64, 162, 158, 166, 57, 45, 38, 168, 
                                    131, 194, 24, 79, 35, 115, 12, 195, 180, 173, 143, 129, 
                                    96, 89, 46, 180, 91, 62, 45, 12, 19, 174, 79)
        
        return smb_usage_data
    
    def create_lcu(self, peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost):
        lcu_usage_data = LCUSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                                    161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                                    110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                                    50, 38, 199, 80, 155, 1, 99, 14, 118, 141, 121, 
                                    31, 198, 108, 44, 54, 22, 31)
        
        return lcu_usage_data
    
    def create_smu(self, peak_usage, offpeak_usage, super_offpeak_usage, peak_cost, offpeak_cost, super_offpeak_cost):
        smu_usage_data = SMUSector(21, 96, 50, 170, 38, 180, 190, 176, 139, 9, 47, 149, 
                                    64, 113, 169, 159, 64, 162, 158, 166, 57, 45, 38, 168, 
                                    131, 194, 24, 79, 35, 115, 12, 195, 180, 173, 143, 129, 
                                    96, 89, 46, 180, 91, 62, 45, 12, 19, 174, 79)
        
        return smu_usage_data
    
    def create_decarb_engine():
        origin = "LAX"
        destination = "JFK"
        departure_date = "2024-07-12"
        return_date = "2024-07-14"
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

        total_savings = 0
        for step in decarb_steps:
            this_savings = step.compute_savings()
            total_savings += this_savings
            print(step.generate_step_description())
            print(f"Savings: ${this_savings}")
            print(f"Emissions Savings: {step.compute_emissions_savings()} kg CO2\n")

def main():
    DecarbEngine.create_decarb_engine()
    #(DecarbEngine.run_electric()) 
        
if __name__ == "__main__":
    main()
        

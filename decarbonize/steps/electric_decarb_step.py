from unittest import result
import pandas as pd
from components.electricity.current_price_calculation.current_electricity import CurrentElectricity
from components.electricity.optimization_calculation.electricity_work import ElectricityWork
from components.electricity.current_price_calculation.current_electricity_cca import Currentelectricity_cca
from components.electricity.optimization_calculation.cca_optimized import electricity_cca
from components.electricity.optimization_calculation import *
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType


class ElectricDecarbStep(DecarbStep):

    def __init__(self, user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled,user_current_company, user_current_plan, UseCCA, HasCCA, usage_data, ranking_zscore, difficulty, meter_input, time_in_use, max_15min_usage,cost_optimise,carbon_optimise):
        self.usage_data = usage_data

        self.user_cur_cost = user_cur_cost
        self.kwh_used = kwh_used
        self.user_zip_code = user_zip_code
        self.user_sector = user_sector
        self.user_bundled = user_bundled
        self.user_current_company=user_current_company
        self.user_current_plan = user_current_plan
        self.UseCCA = UseCCA
        self.HasCCA = HasCCA
        self.cost_optimise=cost_optimise
        self.carbon_optimise=carbon_optimise
        
        self.ranking_zscore = ranking_zscore
        self.steps = []
        self.cur_cost = self.get_cur_cost(UseCCA,cost_optimise)
        self.new_cost = self.get_new_cost(HasCCA,cost_optimise)
        self.saving = self.compute_savings()
        self.cur_emission = self.get_carbon_from_electric(kwh_used)
        self.emissions_saved = self.get_electric_carbon_savings()
        self.difficulty = difficulty
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
        new_emissions = self.get_new_electric_emissions()
        description = "zipcode: " + str(self.user_zip_code) + " cur_cost: " + str(self.cur_cost) + " self.new_cost: " + str(self.new_cost)
        super().__init__(DecarbStepType.ELECTRICITY, user_cur_cost, self.new_cost, self.cur_emission, new_emissions, description, self.difficulty)

    def get_cur_cost(self, UseCCA,cost_optimise):
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', self.user_zip_code, self.usage_data)
        ce_cca= Currentelectricity_cca('Electricity Rate Plan.xlsx',self.user_zip_code,self.kwh_used)
        if (cost_optimise==1 or cost_optimise==0.5):
         if UseCCA == 'Yes':
            cur_cost = ce_cca.fetch_total_cost(self.user_zip_code,self.user_sector,self.user_current_company,self.user_current_plan)
            self.steps.append(cur_cost)
         elif UseCCA == 'No':
            cur_cost = ce.check_condition_and_run(self.user_current_plan, self.user_bundled)
            self.steps.append(cur_cost)
         else:
            cur_cost = "0"
         return float(cur_cost)
        else:
           return 0

    def get_new_plan(self, HasCCA):
        ew = ElectricityWork('Electricity Rate Plan.xlsx', self.user_zip_code,self.usage_data)
        switch_cca=electricity_cca('Electricity Rate Plan.xlsx', self.cost_optimise,self.carbon_optimise)
        
        if HasCCA == 'Yes':
            plan= switch_cca.get_optimized_plan(self.user_zip_code, self.user_sector)
            self.steps.append(plan)
        elif HasCCA == 'No':
            plan= ew.check_condition_and_run(self.user_sector, self.user_bundled)
            ew.print_plan(plan)
            self.steps.append(plan)
        else:
            plan=None
        return plan
    
    def get_new_cost(self, HasCCA,cost_optimise):
        ew = ElectricityWork('Electricity Rate Plan.xlsx', self.user_zip_code,self.usage_data)
        switch_cca=electricity_cca('Electricity Rate Plan.xlsx', self.cost_optimise,self.carbon_optimise)
        if(cost_optimise==1 or cost_optimise==0.5):
         if HasCCA == 'Yes':
            new_cost = switch_cca.get_optimized_plan_cost(self.user_zip_code, self.user_sector,self.kwh_used)
            self.steps.append(new_cost)
         elif HasCCA == 'No':
            new_plan= ew.check_condition_and_run(self.user_sector, self.user_bundled)
            new_cost=new_plan[1]
            self.steps.append(new_cost)
            
         else:
             new_cost = 0
         return new_cost

   
    def compute_savings(self):
        new_plan=self.get_new_plan(self.HasCCA)
        current_cost=self.get_cur_cost(self.UseCCA,self.cost_optimise)
        new_cost=self.get_new_cost(self.HasCCA,self.cost_optimise)
        if(current_cost!=0 and new_cost!=0):
         saving = (current_cost - new_cost)/current_cost * self.user_cur_cost
        
        #print(new_plan)
        #print(current_cost)
        #print(new_cost)
        #print(saving)
         return saving
    
    def get_current_renewable_percentage(self, UseCCA, user_zip_code,carbon_optimise):
        if (carbon_optimise==1 or carbon_optimise==0.5):
         if UseCCA == 'Yes':
            cca_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='CCA')
            joint_rate_plan_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name = 'Joint Rate Plan')
            plan_column = None

            for column in cca_df.columns:
                if user_zip_code in cca_df[column].values:
                    plan_column = column
                    break
       
            if plan_column is None:
                return "No matching CCA zipcode found."
       
            if plan_column in joint_rate_plan_df['Location'].values:
                current_renewable_percentage = joint_rate_plan_df.loc[joint_rate_plan_df['Location'] == plan_column, 'Renewable Energy Percentage'].values[0]
                return float(current_renewable_percentage)
            else:
                return f"No matching location found for {plan_column}."
       
         elif UseCCA == 'No':
            joint_rate_plan_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name = 'Joint Rate Plan')
            current_renewable_percentage = joint_rate_plan_df.loc[joint_rate_plan_df['Electrical Company Name'] == 'PG&E', 'Renewable Energy Percentage'].values[0]
            return float(current_renewable_percentage)
         else:
            return "Error, please reanswer the UseCCA question."
        else:
         return 0
   
    def get_new_renewable(self,carbon_optimise):
        #new_renewable = 56
        #return new_renewable
        if (carbon_optimise==1 or carbon_optimise==0.5):
         if self.HasCCA=='Yes':
            renew_cca=electricity_cca('Electricity Rate Plan.xlsx', self.cost_optimise,self.carbon_optimise)
            new_renewable = renew_cca.get_optimized_renewable(self.user_zip_code, self.user_sector)
            return float(new_renewable)
       
         elif self.HasCCA == 'No':
            joint_rate_plan_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name = 'Joint Rate Plan')
            current_renewable_percentage = joint_rate_plan_df.loc[joint_rate_plan_df['Electrical Company Name'] == 'PG&E', 'Renewable Energy Percentage'].values[0]
            return float(current_renewable_percentage)
         else:
            print("Error, please reanswer the UseCCA question.")
        else:
         return 0
   
    def get_carbon_from_electric(self, kwh_used):
        # Make API request for electric
        # TODO fix with API call
        cur_emission = self.kwh_used * 1.5
        return cur_emission

    def get_electric_carbon_savings(self):
        current_renewable_percentage = float(self.get_current_renewable_percentage(self.UseCCA, self.user_zip_code,self.carbon_optimise))
        new_renewable = float(self.get_new_renewable(self.carbon_optimise))
        carbon_from_electric = float(self.get_carbon_from_electric(self.kwh_used))
        if(new_renewable!=0 and current_renewable_percentage!=0):
         emissions_saved = carbon_from_electric * (1 - (new_renewable - current_renewable_percentage) / current_renewable_percentage)
         return emissions_saved
        else:
           return 0
    
    def get_new_electric_emissions(self):
        current_renewable_percentage = float(self.get_current_renewable_percentage(self.UseCCA, self.user_zip_code,self.carbon_optimise))
        new_renewable = float(self.get_new_renewable(self.carbon_optimise))
        carbon_from_electric = float(self.get_carbon_from_electric(self.kwh_used))
        emissions_saved = carbon_from_electric * (1 - (new_renewable - current_renewable_percentage))
        return emissions_saved

import pandas as pd
from components.electricity.current_price_calculation.current_electricity import CurrentElectricity
from components.electricity.optimization_calculation.electricity_work import ElectricityWork
from components.electricity.current_price_calculation.current_electricity_cca import Currentelectricity_cca
from components.electricity.optimization_calculation.cca_optimised import electricity_cca
from components.electricity.sectors.lcbsector import LCBSector
from components.electricity.sectors.lcusector import LCUSector
from components.electricity.sectors.smbsector import SMBSector
from components.electricity.sectors.smusector import SMUSector
from components.electricity.optimization_calculation import *
class ElectricDecarbStep():

    def __init__(self, user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled,user_current_company, user_current_plan,user_cost_weight,user_renewable_weight, UseCCA, HasCCA, lcb_usage_data, smb_usage_data, lcu_usage_data, smu_usage_data, ranking_zscore):
        
        self.user_cur_cost = user_cur_cost
        self.kwh_used = kwh_used
        self.user_zip_code = user_zip_code
        self.user_sector = user_sector
        self.user_bundled = user_bundled
        self.user_current_company=user_current_company
        self.user_current_plan = user_current_plan
        self.user_cost_weight=user_cost_weight
        self.user_renewable_weight=user_renewable_weight
        self.UseCCA = UseCCA
        self.HasCCA = HasCCA
        self.lcb_usage_data = lcb_usage_data
        self.smb_usage_data = smb_usage_data
        self.lcu_usage_data = lcu_usage_data
        self.smu_usage_data = smu_usage_data
        self.ranking_zscore = ranking_zscore
        self.steps = []
        self.cur_cost = self.get_cur_cost(UseCCA)
        self.new_cost = self.get_new_cost(HasCCA)
        self.saving = self.compute_electricbill_savings()
        get_current_renewable_percentage = self.get_current_renewable_percentage(UseCCA, user_zip_code)
        new_renewable = self.get_new_renewable()
        self.cur_emission = self.get_carbon_from_electric(kwh_used)
        self.emissions_saved = self.get_new_carbon_from_electric()
        
        

    def get_cur_cost(self, UseCCA):
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', self.user_zip_code, self.lcb_usage_data, self.smb_usage_data, self.lcu_usage_data, self.smu_usage_data)
        ce_cca= Currentelectricity_cca('Electricity Rate Plan.xlsx',self.user_zip_code)
        lcb_sector = self.lcb_usage_data
        smb_sector = self.smb_usage_data
        if UseCCA == 'Yes':
            cur_cost = ce_cca.fetch_total_cost(self.user_zip_code,self.user_sector,self.user_current_plan,self.user_current_company)
            self.steps.append(cur_cost)
        elif UseCCA == 'No':
            cur_cost = ce.check_condition_and_run(self.user_current_plan)
            self.steps.append(cur_cost)
        else:
            pass
        return cur_cost

    def get_new_plan(self, HasCCA):
        ew = ElectricityWork('Electricity Rate Plan.xlsx', self.user_zip_code,self.lcb_usage_data,self.smb_usage_data,self.lcu_usage_data,self.smu_usage_data)
        switch_cca=electricity_cca('Electricity Rate Plan.xlsx', user_cost_weight,user_renewable_weight)
        
        if HasCCA == 'Yes':
            new_cost = switch_cca.get_optimized_plan(self.user_sector, self.user_current_company,self.user_zip_code,self.user_current_plan,self.user_cost_weight, self.user_renewable_weight)
            self.steps.append(new_cost)
        elif HasCCA == 'No':
            new_cost = ew.check_condition_and_run(self.user_sector, self.user_bundled)
            plan=ew.print_plan()
            self.steps.append(plan)
        else:
            pass
        return plan
    
    def get_new_cost(self, HasCCA):
        ew = ElectricityWork('Electricity Rate Plan.xlsx', self.user_zip_code,self.lcb_usage_data,self.smb_usage_data,self.lcu_usage_data,self.smu_usage_data)
        switch_cca=electricity_cca('Electricity Rate Plan.xlsx', self.user_cost_weight, self.user_renewable_weight)
        
        if HasCCA == 'Yes':
            new_cost = switch_cca.get_optimized_plan(self.user_sector, self.user_current_company,self.user_zip_code,self.user_current_plan,self.user_cost_weight, self.user_renewable_weight)
            self.steps.append(new_cost)
        elif HasCCA == 'No':
            new_cost = ew.check_condition_and_run(self.user_sector, self.user_bundled)
            self.steps.append(new_cost)
        else:
            pass
        return new_cost


    def compute_electricbill_savings(self):
        current_cost=self.get_cur_cost(self.UseCCA)
        new_cost=self.get_new_cost(self.HasCCA)
        saving = (current_cost - new_cost)/current_cost * self.user_cur_cost
        return saving
    
    def get_current_renewable_percentage(self, UseCCA, user_zip_code):
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
            return f"Error, please reanswer the UseCCA question."
   
    def get_new_renewable(self):
        #new_renewable = 56
        #return new_renewable
        if HasCCA=='Yes':
            new_renewable=electricity_cca('Electricity Rate Plan.xlsx', self.user_cost_weight, self.user_renewable_weight)
       
        elif HasCCA == 'No':
            joint_rate_plan_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name = 'Joint Rate Plan')
            current_renewable_percentage = joint_rate_plan_df.loc[joint_rate_plan_df['Electrical Company Name'] == 'PG&E', 'Renewable Energy Percentage'].values[0]
            return float(current_renewable_percentage)
        else:
            return f"Error, please reanswer the UseCCA question."
   
   
    def get_carbon_from_electric(self, kwh_used):
        # Make API request for electric
        # TODO fix with API call
        cur_emission = self.kwh_used * 1.5
        return cur_emission


    def get_new_carbon_from_electric(self):


        current_renewable_percentage = float(self.get_current_renewable_percentage(self.UseCCA, self.user_zip_code))
        new_renewable = float(self.get_new_renewable())
        carbon_from_electric = float(self.get_carbon_from_electric(self.kwh_used))


        emissions_saved = carbon_from_electric * (new_renewable - current_renewable_percentage)
        return emissions_saved

user_zip_code = 95948
user_sector = 'Large Commercial and Industrial'
user_bundled = 'Yes'
user_current_plan = 'B19TVB'
kwh_used = 10000
user_cur_cost = 100000
difficulty = 2
user_cur_renewable = 0.1
ranking_zscore = 10

user_current_company = 'PG&E'
user_cost_weight = 0.6
user_renewable_weight = 0.4 

UseCCA = 'No'
HasCCA = 'No'

lcb_usage_data = LCBSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                            161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                            110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                            50, 38, 199, 80, 155,1)
smb_usage_data = SMBSector(21, 96, 50, 170, 38, 180, 190, 176, 139, 9, 47, 149, 
                            64, 113, 169, 159, 64, 162, 158, 166, 57, 45, 38, 168, 
                            131, 194, 24, 79, 35, 115, 12, 195, 180, 173, 143, 129, 
                            96, 89, 46, 180, 91, 62, 45, 12, 19, 174, 79)
lcu_usage_data = LCUSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                            161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                            110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                            50, 38, 199, 80, 155, 1, 99, 14, 118, 141, 121, 
                            31, 198, 108, 44, 54, 22, 31)
smu_usage_data = SMUSector(21, 96, 50, 170, 38, 180, 190, 176, 139, 9, 47, 149, 
                            64, 113, 169, 159, 64, 162, 158, 166, 57, 45, 38, 168, 
                            131, 194, 24, 79, 35, 115, 12, 195, 180, 173, 143, 129, 
                            96, 89, 46, 180, 91, 62, 45, 12, 19, 174, 79)

test = ElectricDecarbStep(user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled, user_current_company, 
                        user_current_plan, user_cost_weight,user_renewable_weight, UseCCA, HasCCA, lcb_usage_data, smb_usage_data, lcu_usage_data, 
                        smu_usage_data, ranking_zscore)        
test.compute_electricbill_savings()





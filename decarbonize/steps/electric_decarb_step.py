
from components.electricity.current_price_calculation.current_electricity import CurrentElectricity
from components.electricity.optimization_calculation.electricity_work import ElectricityWork
from components.electricity.sectors.lcbsector import LCBSector
from components.electricity.sectors.lcusector import LCUSector
from components.electricity.sectors.smbsector import SMBSector
from components.electricity.sectors.smusector import SMUSector
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType
from components.electricity.optimization_calculation import *
class ElectricDecarbStep():

    def __init__(self, user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled, user_current_plan, UseCCA, HasCCA, lcb_usage_data, smb_usage_data, lcu_usage_data, smu_usage_data, ranking_zscore):
        
        self.user_cur_cost = user_cur_cost
        self.kwh_used = kwh_used
        self.user_zip_code = user_zip_code
        self.user_sector = user_sector
        self.user_bundled = user_bundled
        self.user_current_plan = user_current_plan
        self.UseCCA = UseCCA
        self.HasCCA = HasCCA
        self.lcb_usage_data = lcb_usage_data
        self.smb_usage_data = smb_usage_data
        self.lcu_usage_data = lcu_usage_data
        self.smu_usage_data = smu_usage_data
        self.ranking_zscore = ranking_zscore
        self.cur_cost = self.get_cur_cost(UseCCA)
        self.new_cost = self.get_new_cost(HasCCA)
        self.saving = self.compute_electricbill_savings()
        self.cur_renewable = self.get_cur_renewable(UseCCA, user_zip_code)
        self.new_renewable = self.get_new_renewable()
        self.cur_emission = self.get_carbon_from_electric(kwh_used)
        self.emissions_saved = self.get_new_carbon_from_electric()
        

    def get_cur_cost(self, UseCCA):
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', self.user_zip_code)
        lcb_sector = self.lcb_usage_data
        smb_sector = self.smb_usage_data
        if UseCCA == 'Yes':
            cur_cost = []#Gowri to do (with CCA)(e.x. user_current_bill_price * (ratio_of_CCA_A1_plan / ratio_of_PGE_A1_plan))
            self.steps.append(cur_cost)
        elif UseCCA == 'No':
            cur_cost = ce.check_condition_and_run(self.user_current_plan)
            self.steps.append(cur_cost)
        else:
            pass
        return cur_cost

    def get_new_cost(self, HasCCA):
        ew = ElectricityWork('Electricity Rate Plan.xlsx', self.user_zip_code)
        if HasCCA == 'Yes':
            new_cost = []#Gowri to do(with CCA, switch plan switch company)
            self.steps.append(new_cost)
        elif HasCCA == 'No':
            new_cost = ew.check_condition_and_run(self.user_sector, self.user_bundled)
            self.steps.append(new_cost)
        else:
            pass
        return new_cost

    def compute_electricbill_savings(self):
        saving = (self.get_cur_cost(self.UseCCA) - self.get_new_cost(self.HasCCA))/self.get_cur_cost(self.UseCCA) * self.user_cur_cost
        return saving
    
    def get_cur_renewable(self, UseCCA, user_zip_code):
        cur_renewable = 48
        return cur_renewable
    
    def get_new_renewable(self):
        new_renewable = 56
        return new_renewable
    
    def get_carbon_from_electric(self, kwh_used):
        # Make API request for electric
        # TODO fix with API call
        cur_emission = self.kwh_used * 1.5
        return cur_emission

    def get_new_carbon_from_electric(self):
       
        emissions_saved =  self.get_carbon_from_electric(self.kwh_used) * (self.get_new_renewable() - self.get_cur_renewable(self.UseCCA, self.user_zip_code))
        
        return emissions_saved

user_zip_code = 95948
user_sector = 'Large Commercial and Industrial'
user_bundled = 'Yes'
user_current_plan = 'B19_SV'
kwh_used = 10000
user_cur_cost = 100000
difficulty = 2
user_cur_renewable = 0.1
ranking_zscore = 10

UseCCA = 'No'
HasCCA = 'No'

lcb_usage_data = LCBSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                       161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                      110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                      50, 38, 199, 80, 155, 1)
smb_usage_data = SMBSector(20, 30, 101,37, 167, 174,41,179,187,140, 165,
                        174,174, 185, 196,166, 8, 71,184, 81, 158,28, 57, 122,
                        170, 21, 31,69, 110, 28,70, 45, 54,73, 76, 178,13, 88,
                        23,156, 96, 169,181, 56, 169,107, 119)
lcu_usage_data = LCUSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                        161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                        110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                        50, 38, 199, 80, 155, 1)
smu_usage_data = SMUSector(20, 30, 101,37, 167, 174,41,179,187,140, 165,
                        174,174, 185, 196,166, 8, 71,184, 81, 158,28, 57, 122,
                        170, 21, 31,69, 110, 28,70, 45, 54,73, 76, 178,13, 88,
                        23,156, 96, 169,181, 56, 169,107, 119, 127, 1)

test = ElectricDecarbStep(user_cur_cost, kwh_used, user_zip_code, user_sector, user_bundled, 
                          user_current_plan, UseCCA, HasCCA, lcb_usage_data, smb_usage_data, lcu_usage_data, 
                          smu_usage_data, ranking_zscore)
test.compute_electricbill_savings()

# User Input, now is fake




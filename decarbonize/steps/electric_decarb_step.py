
from steps.decarb_step import DecarbStep
from steps.decarb_step_type import DecarbStepType

class ElectricDecarbStep(DecarbStep):
    def __init__(self, cur_cost, new_cost, cur_renewable, new_renewable, kwh_used, description, difficulty):
        self.cur_renewable = cur_renewable
        self.new_renewable = new_renewable
        self.kwh_used = kwh_used
        cur_emissions = self.get_carbon_from_electric(kwh_used)
        new_emissions = self.get_new_carbon_from_electric(cur_emissions, cur_renewable, new_renewable)
        super().__init__(DecarbStepType.ELECTRICITY, cur_cost, new_cost, cur_emissions, new_emissions, description, difficulty)
        self.steps = []
        self.cur_cost = self.get_cur_cost(UseCCA)
        self.new_cost = self.get_new_cost(HasCCA)

    def get_cur_cost(self, UseCCA):
        ce = CurrentElectricity('Electricity Rate Plan.xlsx', user_zip_code)
        lcb_sector = lcb_usage_data
        smb_sector = smb_usage_data
        if UseCCA == 'Yes':
            cur_cost = #Gowri to do (with CCA)(e.x. user_current_bill_price * (ratio_of_CCA_A1_plan / ratio_of_PGE_A1_plan))
            self.steps.append(cur_cost)
        elif UseCCA == 'No':
            cur_cost = ce.check_condition_and_run(user_current_plan)
            self.steps.append(cur_cost)
        else:
            pass
        return cur_cost

    def get_new_cost(self, HasCCA):
        ew = ElectricityWork('Electricity Rate Plan.xlsx', user_zip_code)
        lcb_sector = lcb_usage_data
        smb_sector = smb_usage_data
        lcu_sector = lcu_usage_data
        smu_sector = smu_usage_data
        if HasCCA == 'Yes':
            new_cost = #Gowri to do(with CCA, switch plan switch company)
            self.steps.append(new_cost)
        elif HasCCA == 'No':
            new_cost = ew.check_condition_and_run(user_sector, user_bundled)
            self.steps.append(new_cost)
        else:
            pass
        return new_cost

    def compute_electricbill_savings(self):
        return (self.cur_cost - self.new_cost)/self.cur_cost * current_electricbill_price

    def generate_step_description(self):
        base_description = super().generate_step_description()
        return f"{base_description}"
    
    def get_carbon_from_electric(self, kwh_used):
        # Make API request for electric
        # TODO fix with API call
        return kwh_used * 1.5

    def get_new_carbon_from_electric(self, cur_emissions, cur_renewable, new_renewable):
        cur_emissions = cur_emissions * (new_renewable - cur_renewable)
        return cur_emissions


# User Input, now is fake

user_zip_code = 95347
user_sector = 'Large Commercial and Industrial'
user_bundled = 'Yes'
user_current_plan = 'B19_SV'
kwh_used = 10000
current_electricbill_price = 100000

UseCCA = 'No'
HasCCA = 'No'

lcb_usage_data = LCBSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                           161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                           110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                           50, 38, 199, 80, 155)
smb_usage_data = SMBSector(20, 30, 101,37, 167, 174,41,179,187,140, 165,
                           174,174, 185, 196,166, 8, 71,184, 81, 158,28, 57, 122,
                           170, 21, 31,69, 110, 28,70, 45, 54,73, 76, 178,13, 88,
                           23,156, 96, 169,181, 56, 169,107, 119, 127)
lcu_usage_data = LCUSector(162, 76, 181, 101, 61, 37, 9, 78, 65, 13, 29,
                           161, 25, 34, 112, 143, 15, 78, 134, 92, 67, 67,
                           110, 6, 35, 154, 28, 153, 132, 127, 12, 30, 191,
                           50, 38, 199, 80, 155)
smu_usage_data = SMUSector(20, 30, 101,37, 167, 174,41,179,187,140, 165,
                           174,174, 185, 196,166, 8, 71,184, 81, 158,28, 57, 122,
                           170, 21, 31,69, 110, 28,70, 45, 54,73, 76, 178,13, 88,
                           23,156, 96, 169,181, 56, 169,107, 119, 127)


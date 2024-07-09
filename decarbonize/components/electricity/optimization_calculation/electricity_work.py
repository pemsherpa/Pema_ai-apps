# -*- coding: utf-8 -*-
"""Electricity Work

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ePwPoGLE4I2v2nhUDYOAZqynoNYGu0vv
"""

import pandas as pd

from components.electricity.optimization_calculation.lcbelectricityrateplan import LCBElectricityRatePlan
from components.electricity.optimization_calculation.lcuelectricityrateplan import LCUElectricityRatePlan
from components.electricity.optimization_calculation.smuelectricityrateplan import SMUElectricityRatePlan
from components.electricity.optimization_calculation.smbelectricityrateplan import SMBElectricityRatePlan
from components.electricity.sectors.lcbsector import LCBSector
from components.electricity.sectors.lcusector import LCUSector
from components.electricity.sectors.smbsector import SMBSector
from components.electricity.sectors.smusector import SMUSector

class ElectricityWork:
    def __init__(self, file_path, user_zip_code):
        self.file_path = file_path
        self.sheets = pd.read_excel(self.file_path, sheet_name=None)
        self.pge_service_df = self.sheets['PG&E Service Area']
        self.cca_df = self.sheets['CCA']
        self.joint_rate_plan_df = self.sheets['Joint Rate Plan']
        self.bundled_peak_time_price_df = self.sheets['Bundled Peak Time Price']
        self.unbundled_peak_time_price_df = self.sheets['Unbundled Peak Time Price']
        self.user_zip_code = user_zip_code

    def check_zip_code(self, user_zip_code):
        if user_zip_code in self.pge_service_df['PG&E Service area Zip Code'].values:
            return "In PG&E service"
        else:
            return "Not in PG&E service"

    def match_cca_service(self, user_zip_code):
        for column in self.cca_df.columns:
            if user_zip_code in self.cca_df[column].values:
                return f"Matched in CCA: {column}"
        return "No CCA"

    def get_matched_rows(self, user_zip_code, user_sector, user_bundled):
        result1 = self.check_zip_code(user_zip_code)
        result2 = self.match_cca_service(user_zip_code)

        if "Matched in CCA" in result2:
            matched_column = result2.split(": ")[1]
            location_matched_rows = self.joint_rate_plan_df[self.joint_rate_plan_df['Location'] == matched_column]
            final_matched_rows = location_matched_rows[location_matched_rows['Sector'] == user_sector]
            return final_matched_rows
        elif "No CCA" in result2:
            if user_bundled == "Yes":
                sector_matched_rows = self.bundled_peak_time_price_df[self.bundled_peak_time_price_df['Sector'] == user_sector]
            else:
                sector_matched_rows = self.unbundled_peak_time_price_df[self.unbundled_peak_time_price_df['Sector'] == user_sector]
            return sector_matched_rows
        else:
            return "No matching rows in joint rate plan", "No matching rows in joint rate comparison"

    def create_smb_sector(self, A1NTBStotal_usage, A1NTBWtotal_usage, A1BSpeak_usage,
                 A1BSpartpeak_usage, A1BSoffpeak_usage, A1BWpartpeak_usage,
                 A1BWoffpeak_usage, B1BSpeak_usage, B1BSpartpeak_usage, B1BSoffpeak_usage,
                 B1BWpeak_usage, B1BWsuperoffpeak_usage, B1BWoffpeak_usage,
                 B1STBSpeak_usage, B1STBSpartpeak_usage, B1STBSoffpeak_usage,
                 B1STBWpeak_usage, B1STBWpartpeak_usage, B1STBWsuperoffpeak_usage,
                 B1STBWoffpeak_usage, B6BSpeak_usage, B6BSoffpeak_usage,
                 B6BWpeak_usage, B6BWsuperoffpeak_usage,B6BWoffpeak_usage,
                 B10SVBSpeak_usage,B10SVBSpartpeak_usage,B10SVBSoffpeak_usage,
                 B10SVBWpeak_usage, B10SVBWsuperoffpeak_usage, B10SVBWoffpeak_usage,
                 B10PVBSpeak_usage,B10PVBSpartpeak_usage,B10PVBSoffpeak_usage,
                 B10PVBWpeak_usage,B10PVBWsuperoffpeak_usage,B10PVBWoffpeak_usage,
                 B10TVBSpeak_usage, B10TVBSpartpeak_usage,B10TVBSoffpeak_usage,
                 B10TVBWpeak_usage,B10TVBWsuperoffpeak_usage, B10TVBWoffpeak_usage,
                 meter_input,time_in_use, max_15min_usage,B1STB_highest_demand_15mins):
        smb_sector = SMBSector(A1NTBStotal_usage, A1NTBWtotal_usage, A1BSpeak_usage,
                 A1BSpartpeak_usage, A1BSoffpeak_usage, A1BWpartpeak_usage,
                 A1BWoffpeak_usage, B1BSpeak_usage, B1BSpartpeak_usage, B1BSoffpeak_usage,
                 B1BWpeak_usage, B1BWsuperoffpeak_usage, B1BWoffpeak_usage,
                 B1STBSpeak_usage, B1STBSpartpeak_usage, B1STBSoffpeak_usage,
                 B1STBWpeak_usage, B1STBWpartpeak_usage, B1STBWsuperoffpeak_usage,
                 B1STBWoffpeak_usage, B6BSpeak_usage, B6BSoffpeak_usage,
                 B6BWpeak_usage, B6BWsuperoffpeak_usage,B6BWoffpeak_usage,
                 B10SVBSpeak_usage,B10SVBSpartpeak_usage,B10SVBSoffpeak_usage,
                 B10SVBWpeak_usage, B10SVBWsuperoffpeak_usage, B10SVBWoffpeak_usage,
                 B10PVBSpeak_usage,B10PVBSpartpeak_usage,B10PVBSoffpeak_usage,
                 B10PVBWpeak_usage,B10PVBWsuperoffpeak_usage,B10PVBWoffpeak_usage,
                 B10TVBSpeak_usage, B10TVBSpartpeak_usage,B10TVBSoffpeak_usage,
                 B10TVBWpeak_usage,B10TVBWsuperoffpeak_usage, B10TVBWoffpeak_usage,
                 meter_input,time_in_use, max_15min_usage,B1STB_highest_demand_15mins)
        return smb_sector

    def create_lcb_sector(self, B19SVBSpeak_usage, B19SVBSpartpeak_usage, B19SVBSoffpeak_usage,
                 B19SVBWpeak_usage,B19SVBWsuperoffpeak_usage,B19SVBWoffpeak_usage,
                 B19PVBSpeak_usage,B19PVBSpartpeak_usage,B19PVBSoffpeak_usage,
                 B19PVBWpeak_usage,B19PVBWsuperoffpeak_usage,B19PVBWoffpeak_usage,
                 B19TVBSpeak_usage,B19TVBSpartpeak_usage,B19TVBSoffpeak_usage,
                 B19TVBWpeak_usage,B19TVBWsuperoffpeak_usage,B19TVBWoffpeak_usage,
                 B20SVBSpeak_usage, B20SVBSpartpeak_usage, B20SVBSoffpeak_usage,
                 B20SVBWpeak_usage,B20SVBWsuperoffpeak_usage,B20SVBWoffpeak_usage,
                 B20PVBSpeak_usage,B20PVBSpartpeak_usage,B20PVBWpeak_usage,
                 B20PVBWsuperoffpeak_usage,B20PVBWoffpeak_usage,
                 B20TVBSpeak_usage,B20TVBSpartpeak_usage,B20TVBSoffpeak_usage,
                 B20TVBWpeak_usage,B20TVBWsuperoffpeak_usage,B20TVBWoffpeak_usage,
                 meter_input,time_in_use,max_15min_usage):
        lcb_sector = LCBSector(B19SVBSpeak_usage, B19SVBSpartpeak_usage, B19SVBSoffpeak_usage,
                 B19SVBWpeak_usage,B19SVBWsuperoffpeak_usage,B19SVBWoffpeak_usage,
                 B19PVBSpeak_usage,B19PVBSpartpeak_usage,B19PVBSoffpeak_usage,
                 B19PVBWpeak_usage,B19PVBWsuperoffpeak_usage,B19PVBWoffpeak_usage,
                 B19TVBSpeak_usage,B19TVBSpartpeak_usage,B19TVBSoffpeak_usage,
                 B19TVBWpeak_usage,B19TVBWsuperoffpeak_usage,B19TVBWoffpeak_usage,
                 B20SVBSpeak_usage, B20SVBSpartpeak_usage, B20SVBSoffpeak_usage,
                 B20SVBWpeak_usage,B20SVBWsuperoffpeak_usage,B20SVBWoffpeak_usage,
                 B20PVBSpeak_usage,B20PVBSpartpeak_usage,B20PVBWpeak_usage,
                 B20PVBWsuperoffpeak_usage,B20PVBWoffpeak_usage,
                 B20TVBSpeak_usage,B20TVBSpartpeak_usage,B20TVBSoffpeak_usage,
                 B20TVBWpeak_usage,B20TVBWsuperoffpeak_usage,B20TVBWoffpeak_usage,
                 meter_input,time_in_use,max_15min_usage)
        return lcb_sector

    def create_smu_sector(self, A1NTUStotal_usage, A1NTUWtotal_usage, A1USpeak_usage,
                 A1USpartpeak_usage, A1USoffpeak_usage, A1UWpartpeak_usage,
                 A1UWoffpeak_usage, B1USpeak_usage, B1USpartpeak_usage, B1USoffpeak_usage,
                 B1UWpeak_usage, B1UWsuperoffpeak_usage, B1UWoffpeak_usage,
                 B1STUSpeak_usage, B1STUSpartpeak_usage, B1STUSoffpeak_usage,
                 B1STUWpeak_usage, B1STUWpartpeak_usage, B1STUWsuperoffpeak_usage,
                 B1STUWoffpeak_usage, B6USpeak_usage, B6USoffpeak_usage,
                 B6UWpeak_usage, B6UWsuperoffpeak_usage,B6UWoffpeak_usage,
                 B10SVUSpeak_usage,B10SVUSpartpeak_usage,B10SVUSoffpeak_usage,
                 B10SVUWpeak_usage, B10SVUWsuperoffpeak_usage, B10SVUWoffpeak_usage,
                 B10PVUSpeak_usage,B10PVUSpartpeak_usage,B10PVUSoffpeak_usage,
                 B10PVUWpeak_usage,B10PVUWsuperoffpeak_usage,B10PVUWoffpeak_usage,
                 B10TVUSpeak_usage, B10TVUSpartpeak_usage,B10TVUSoffpeak_usage,
                 B10TVUWpeak_usage,B10TVUWsuperoffpeak_usage, B10TVUWoffpeak_usage,
                 meter_input,time_in_use, max_15min_usage,B1STU_highest_demand_15mins):
        smu_sector= SMUSector(A1NTUStotal_usage, A1NTUWtotal_usage, A1USpeak_usage,
                 A1USpartpeak_usage, A1USoffpeak_usage, A1UWpartpeak_usage,
                 A1UWoffpeak_usage, B1USpeak_usage, B1USpartpeak_usage, B1USoffpeak_usage,
                 B1UWpeak_usage, B1UWsuperoffpeak_usage, B1UWoffpeak_usage,
                 B1STUSpeak_usage, B1STUSpartpeak_usage, B1STUSoffpeak_usage,
                 B1STUWpeak_usage, B1STUWpartpeak_usage, B1STUWsuperoffpeak_usage,
                 B1STUWoffpeak_usage, B6USpeak_usage, B6USoffpeak_usage,
                 B6UWpeak_usage, B6UWsuperoffpeak_usage,B6UWoffpeak_usage,
                 B10SVUSpeak_usage,B10SVUSpartpeak_usage,B10SVUSoffpeak_usage,
                 B10SVUWpeak_usage, B10SVUWsuperoffpeak_usage, B10SVUWoffpeak_usage,
                 B10PVUSpeak_usage,B10PVUSpartpeak_usage,B10PVUSoffpeak_usage,
                 B10PVUWpeak_usage,B10PVUWsuperoffpeak_usage,B10PVUWoffpeak_usage,
                 B10TVUSpeak_usage, B10TVUSpartpeak_usage,B10TVUSoffpeak_usage,
                 B10TVUWpeak_usage,B10TVUWsuperoffpeak_usage, B10TVUWoffpeak_usage,
                 meter_input,time_in_use, max_15min_usage,B1STU_highest_demand_15mins)
        return smu_sector

    def create_lcu_sector(self, B19SVUSpeak_usage, B19SVUSpartpeak_usage, B19SVUSoffpeak_usage,
                 B19SVUWpeak_usage,B19SVUWsuperoffpeak_usage,B19SVUWoffpeak_usage,Summer_highest_usage_B19SV,Winter_highest_usage_B19SV,
                 B19PVUSpeak_usage,B19PVUSpartpeak_usage,B19PVUSoffpeak_usage,
                 B19PVUWpeak_usage,B19PVUWsuperoffpeak_usage,B19PVUWoffpeak_usage,Summer_highest_usage_B19PV,Winter_highest_usage_B19PV,
                 B19TVUSpeak_usage,B19TVUSpartpeak_usage,B19TVUSoffpeak_usage,
                 B19TVUWpeak_usage,B19TVUWsuperoffpeak_usage,B19TVUWoffpeak_usage,Summer_highest_usage_B19TV,Winter_highest_usage_B19TV,
                 B20SVUSpeak_usage, B20SVUSpartpeak_usage, B20SVUSoffpeak_usage,
                 B20SVUWpeak_usage,B20SVUWsuperoffpeak_usage,B20SVUWoffpeak_usage,Summer_highest_usage_B20SV,Winter_highest_usage_B20SV,
                 B20PVUSpeak_usage,B20PVUSpartpeak_usage,B20PVUSoffpeak_usage,
                 B20PVUWpeak_usage,B20PVUWsuperoffpeak_usage,B20PVUWoffpeak_usage,Summer_highest_usage_B20PV,Winter_highest_usage_B20PV,
                 B20TVUSpeak_usage,B20TVUSpartpeak_usage,B20TVUSoffpeak_usage,
                 B20TVUWpeak_usage,B20TVUWsuperoffpeak_usage,B20TVUWoffpeak_usage,Summer_highest_usage_B20TV,Winter_highest_usage_B20TV,
                 meter_input,time_in_use,max_15min_usage):
        lcu_sector = LCUSector(B19SVUSpeak_usage, B19SVUSpartpeak_usage, B19SVUSoffpeak_usage,
                 B19SVUWpeak_usage,B19SVUWsuperoffpeak_usage,B19SVUWoffpeak_usage,Summer_highest_usage_B19SV,Winter_highest_usage_B19SV,
                 B19PVUSpeak_usage,B19PVUSpartpeak_usage,B19PVUSoffpeak_usage,
                 B19PVUWpeak_usage,B19PVUWsuperoffpeak_usage,B19PVUWoffpeak_usage,Summer_highest_usage_B19PV,Winter_highest_usage_B19PV,
                 B19TVUSpeak_usage,B19TVUSpartpeak_usage,B19TVUSoffpeak_usage,
                 B19TVUWpeak_usage,B19TVUWsuperoffpeak_usage,B19TVUWoffpeak_usage,Summer_highest_usage_B19TV,Winter_highest_usage_B19TV,
                 B20SVUSpeak_usage, B20SVUSpartpeak_usage, B20SVUSoffpeak_usage,
                 B20SVUWpeak_usage,B20SVUWsuperoffpeak_usage,B20SVUWoffpeak_usage,Summer_highest_usage_B20SV,Winter_highest_usage_B20SV,
                 B20PVUSpeak_usage,B20PVUSpartpeak_usage,B20PVUSoffpeak_usage,
                 B20PVUWpeak_usage,B20PVUWsuperoffpeak_usage,B20PVUWoffpeak_usage,Summer_highest_usage_B20PV,Winter_highest_usage_B20PV,
                 B20TVUSpeak_usage,B20TVUSpartpeak_usage,B20TVUSoffpeak_usage,
                 B20TVUWpeak_usage,B20TVUWsuperoffpeak_usage,B20TVUWoffpeak_usage,Summer_highest_usage_B20TV,Winter_highest_usage_B20TV,
                 meter_input,time_in_use,max_15min_usage)
        return lcu_sector
    
    def print_result(self, result, keys):
        print("Optimal solution:", result['x'])
        print("Optimal objective value:", result['objective'])
        print("Optimal solution:", {name for i, name in enumerate(keys) if result['x'][i] == 1})
        
    def check_condition_and_run(self, user_sector, user_bundled):
        condition1 = (user_sector == 'Large Commercial and Industrial' and user_bundled == 'Yes')
        condition2 = (user_sector == 'Large Commercial and Industrial' and user_bundled == 'No')
        condition3 = (user_sector == 'Small and Medium Business' and user_bundled == 'Yes')
        condition4 = (user_sector == 'Small and Medium Business' and user_bundled == 'No')

        rate_plan = None 
        keys = []
        if condition1:
            lcb_sector = self.create_lcb_sector()
            rate_plan = LCBElectricityRatePlan(self.file_path, 'Bundled Peak Time Price', lcb_sector)
            keys = ['B19SVB', 'B19PVB', 'B19TVB', 'B19B', 'B20SVB', 'B20PVB', 'B20TVB', 'B20B']            
        elif condition2:
            lcu_sector = self.create_lcu_sector()
            rate_plan = LCUElectricityRatePlan(self.file_path, 'Unbundled Peak Time Price', lcu_sector)
            keys = ['B19SVU', 'B19PVU', 'B19TVU', 'B19U', 'B20SVU', 'B20PVU', 'B20TVU', 'B20U']
        elif condition3:
            smb_sector = self.create_smb_sector()
            rate_plan = SMBElectricityRatePlan(self.file_path, 'Bundled Peak Time Price', smb_sector)
            keys = ['A1NTB', 'A1B', 'B1B', 'B1STB', 'B6B', 'B10SVB', 'B10PVB', 'B10TVB', 'A1NTB_poly', 'A1NTB_single', 'A1B_poly', 'A1B_single', 'B1B_poly', 'B1B_single', 'B1STB_poly', 'B1STB_single', 'B6B_poly', 'B6B_single']
        elif condition4:
            smu_sector = self.create_smu_sector()
            rate_plan = SMUElectricityRatePlan(self.file_path, 'Unbundled Peak Time Price', smu_sector)
            keys = ['A1NTU', 'A1U', 'B1U', 'B1STU', 'B6U', 'B10SVU', 'B10PVU', 'B10TVU', 'A1NTU_poly', 'A1NTU_single', 'A1U_poly', 'A1U_single', 'B1U_poly', 'B1U_single', 'B1STU_poly', 'B1STU_single', 'B6U_poly', 'B6U_single']
        else:
            err_msg = "check_condition_and_run: Condition not met, not running the script."
            print(err_msg)
            raise Exception(err_msg)
        
        result = rate_plan.optimize()     
        self.print_result(result, keys)




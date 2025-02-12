# -*- coding: utf-8 -*-
"""Current Electricity.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gtmH1wBHi6pjwJx0G9AEHpC3kwtTibIP
"""

import pandas as pd
from components.electricity.current_price_calculation.currentlcbelectricityrateplan import currentLCBElectricityRatePlan
from components.electricity.current_price_calculation.currentsmbelectricityrateplan import currentSMBElectricityRatePlan
from components.electricity.current_price_calculation.currentlcuelectricityrateplan import currentLCUElectricityRatePlan
from components.electricity.current_price_calculation.currentsmuelectricityrateplan import currentSMUElectricityRatePlan

class CurrentElectricity:
    def __init__(self, file_path, user_zip_code, usage_data):
        self.file_path = file_path
        self.sheets = pd.read_excel(self.file_path, sheet_name=None)
        self.pge_service_df = self.sheets['PG&E Service Area']
        self.cca_df = self.sheets['CCA']
        self.joint_rate_plan_df = self.sheets['Joint Rate Plan']
        self.bundled_peak_time_price_df = self.sheets['Bundled Peak Time Price']
        self.unbundled_peak_time_price_df = self.sheets['Unbundled Peak Time Price']
        self.user_zip_code = user_zip_code

        self.usage_data = usage_data

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

    def print_result(self, result, keys):
        return result['objective']

    def check_condition_and_run(self, user_current_plan, user_bundled):
        condition1_keys = ['B-19_SV', 'B-19_PV', 'B-19_TV', 'B-19', 'B-20_SV', 'B-20_PV', 'B-20_TV', 'B-20', 'B-19_S','B-20_S', 'B-20_P']
        condition2_keys = ['A-1NT', 'A-1', 'B-1', 'B-1-ST', 'B-6', 'B-10_SV', 'B-10_PV', 'B-10_TV', 'B-10_S']
        condition3_keys=  ['B-19_SV', 'B-19_PV', 'B-19_TV', 'B-19', 'B-20_SV', 'B-20_PV', 'B-20_TV', 'B-20', 'B-19_S','B-20_S', 'B-20_P']
        condition4_keys=  ['A-1NT', 'A-1', 'B-1', 'B-1-ST', 'B-6', 'B-10_SV', 'B-10_PV', 'B-10_TV', 'B-10_S']

        condition1 = user_current_plan in condition1_keys and user_bundled == 'Yes'
        condition2 = user_current_plan in condition2_keys and user_bundled == 'Yes'
        condition3 = user_current_plan in condition3_keys and user_bundled == 'No'
        condition4 = user_current_plan in condition4_keys and user_bundled == 'No'

        rate_plan = None
        keys = []

        if condition1:
            rate_plan = currentLCBElectricityRatePlan(self.file_path, 'Bundled Peak Time Price', self.usage_data)
            keys = condition1_keys
        elif condition2:
            rate_plan = currentSMBElectricityRatePlan(self.file_path, 'Bundled Peak Time Price', self.usage_data)
            keys = condition2_keys
        elif condition3:
            rate_plan = currentLCUElectricityRatePlan(self.file_path, 'Unbundled Peak Time Price', self.usage_data)
            keys = condition3_keys
        elif condition4:
            rate_plan = currentSMUElectricityRatePlan(self.file_path, 'Unbundled Peak Time Price', self.usage_data)
            keys = condition4_keys
        else:
            err_msg = "Current Electricity: Condition not met, not running the script."
            print(err_msg)
            raise Exception(err_msg)
        
        result = rate_plan.currentprice(user_current_plan)
        return result['objective']

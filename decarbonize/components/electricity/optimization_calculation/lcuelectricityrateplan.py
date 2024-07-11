# -*- coding: utf-8 -*-
"""lcuelectricityrateplan.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Qp-O0b-rQg8uyt3AVxWGfQrZVan28m6z
"""

# -*- coding: utf-8 -*-
"""LCU.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wEHOWbSBUGH2MORnrLrAN-0_4-s_pE5D
"""

from scipy.optimize import minimize
from scipy.optimize import Bounds
import pandas as pd

class LCUElectricityRatePlan:
    def __init__(self, file_path, sheet_name, lcu_usage_data):
        self.df = pd.read_excel(file_path, sheet_name=sheet_name)
        self.get_sum()
        self.parameters = {}
        self.lcu_usage_data = lcu_usage_data
        self.load_parameters()

    def get_sum(self):
        col_sum = ['Generation', 'Distribution', 'Transmission', 'Transmission Rate Adjustments',
                   'Reliability Services', 'Public Purpose Programs', 'Nuclear Decommissioning',
                   'Competition Transition Charges', 'Energy Cost Recovery Amount', 'New System Generation Charge', 'Wildfire Fund Charge',
                   'California Climate Credit', 'Wildfire Hardening Charge']
        self.df['sum'] = self.df[col_sum].sum(axis=1)
        return self.df

    def get_parameter(self, sector, plan, season, ptype, phase=None, column='sum'):
        query = f"Sector == '{sector}' and Plan == '{plan}' and Season == '{season}' and Type == '{ptype}'"
        if phase:
            query += f" and Phase == '{phase}'"
        return self.df.query(query)[column].values[0]

    def load_parameters(self):
        # Load all required parameters
        self.parameters['B19SVUSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Peak')
        self.parameters['B19SVUSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Part-Peak')
        self.parameters['B19SVUSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Off-Peak')
        self.parameters['B19SVUWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Winter', 'Peak')
        self.parameters['B19SVUWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Winter', 'Super-Off-Peak')
        self.parameters['B19SVUWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Winter', 'Off-Peak')
        self.parameters['B19SVU_CCR'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer','Peak', column='Customer Charge Rate')
        self.parameters['B19SVUS_demand_rate'] = 39.16
        self.parameters['B19SVUW_demand_rate'] = 42.18
        self.parameters['B19PVUSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Peak')
        self.parameters['B19PVUSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Part-Peak')
        self.parameters['B19PVUSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Off-Peak')
        self.parameters['B19PVUWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Winter', 'Peak')
        self.parameters['B19PVUWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Winter', 'Super-Off-Peak')
        self.parameters['B19PVUWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Winter', 'Off-Peak')
        self.parameters['B19PVU_CCR'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer','Peak', column='Customer Charge Rate')
        self.parameters['B19PVUS_demand_rate'] = 31.09
        self.parameters['B19PVUW_demand_rate'] = 33.28
        self.parameters['B19TVUSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Peak')
        self.parameters['B19TVUSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Part-Peak')
        self.parameters['B19TVUSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Off-Peak')
        self.parameters['B19TVUWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Winter', 'Peak')
        self.parameters['B19TVUWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Winter', 'Super-Off-Peak')
        self.parameters['B19TVUWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Winter', 'Off-Peak')
        self.parameters['B19TVU_CCR'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer','Peak', column='Customer Charge Rate')
        self.parameters['B19TVUS_demand_rate'] = 19.72
        self.parameters['B19TVUW_demand_rate'] = 21.57
        self.parameters['B20SVUSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Peak')
        self.parameters['B20SVUSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Part-Peak')
        self.parameters['B20SVUSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Off-Peak')
        self.parameters['B20SVUWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Winter', 'Peak')
        self.parameters['B20SVUWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Winter', 'Super-Off-Peak')
        self.parameters['B20SVUWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Winter', 'Off-Peak')
        self.parameters['B20SVU_CCR'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer','Peak', column='Customer Charge Rate')
        self.parameters['B20SVUS_demand_rate'] = 41.84
        self.parameters['B20SVUW_demand_rate'] = 44.87
        self.parameters['B20PVUSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Peak')
        self.parameters['B20PVUSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Part-Peak')
        self.parameters['B20PVUSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Off-Peak')
        self.parameters['B20PVUWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Winter', 'Peak')
        self.parameters['B20PVUWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Winter', 'Super-Off-Peak')
        self.parameters['B20PVUWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Winter', 'Off-Peak')
        self.parameters['B20PVU_CCR'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer','Peak', column='Customer Charge Rate')
        self.parameters['B20PVUS_demand_rate'] = 37.14
        self.parameters['B20PVUW_demand_rate'] = 43.26
        self.parameters['B20TVUSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Peak')
        self.parameters['B20TVUSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Part-Peak')
        self.parameters['B20TVUSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Off-Peak')
        self.parameters['B20TVUWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Winter', 'Peak')
        self.parameters['B20TVUWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Winter', 'Super-Off-Peak')
        self.parameters['B20TVUWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Winter', 'Off-Peak')
        self.parameters['B20TVU_CCR'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer','Peak', column='Customer Charge Rate')
        self.parameters['B20TVUS_demand_rate'] = 21.25
        self.parameters['B20TVUW_demand_rate'] = 24.99

    def objective(self, x):
        B19SVU, B19PVU, B19TVU, B19U, B20SVU, B20PVU, B20TVU,B20U=x
        lcu_usage_data = self.lcu_usage_data
        meter_input, time_in_use = lcu_usage_data['meter_input'], lcu_usage_data['time_in_use']

        B19SVUSprice = (self.parameters['B19SVUSpeakprice'] * lcu_usage_data['B19SVUSpeak_usage'] +
                     self.parameters['B19SVUSpartpeakprice'] * lcu_usage_data['B19SVUSpartpeak_usage'] +
                     self.parameters['B19SVUSoffpeakprice'] * lcu_usage_data['B19SVUSoffpeak_usage'])
        B19SVUWprice = (self.parameters['B19SVUWpeakprice'] * lcu_usage_data['B19SVUWpeak_usage'] +
                      self.parameters['B19SVUWsuperoffpeakprice'] * lcu_usage_data['B19SVUWsuperoffpeak_usage'] +
                       self.parameters['B19SVUWoffpeakprice'] * lcu_usage_data['B19SVUWoffpeak_usage'])

        B19SVU_demand_charge= (self.parameters['B19SVUS_demand_rate'] * lcu_usage_data['Summer_highest_usage_B19SV']+self.parameters['B19SVUW_demand_rate'] * lcu_usage_data['Winter_highest_usage_B19SV'])

        B19SVUprice = B19SVUSprice + B19SVUWprice + (self.parameters['B19SVU_CCR'] * meter_input * time_in_use)+B19SVU_demand_charge

        B19PVUSprice = (self.parameters['B19PVUSpeakprice'] * lcu_usage_data['B19PVUSpeak_usage'] +
                     self.parameters['B19PVUSpartpeakprice'] * lcu_usage_data['B19PVUSpartpeak_usage'] +
                     self.parameters['B19PVUSoffpeakprice'] * lcu_usage_data['B19PVUSoffpeak_usage'])
        B19PVUWprice = (self.parameters['B19PVUWpeakprice'] * lcu_usage_data['B19PVUWpeak_usage'] +
                      self.parameters['B19PVUWsuperoffpeakprice'] * lcu_usage_data['B19PVUWsuperoffpeak_usage'] +
                       self.parameters['B19PVUWoffpeakprice'] * lcu_usage_data['B19PVUWoffpeak_usage'])

        B19PVU_demand_charge= (self.parameters['B19PVUS_demand_rate'] * lcu_usage_data['Summer_highest_usage_B20PV']+self.parameters['B19PVUW_demand_rate'] * lcu_usage_data['Winter_highest_usage_B20PV'])

        B19PVUprice = B19PVUSprice + B19PVUWprice + (self.parameters['B19PVU_CCR'] * meter_input * time_in_use)+B19PVU_demand_charge

        B19TVUSprice = (self.parameters['B19TVUSpeakprice'] * lcu_usage_data['B19TVUSpeak_usage'] +
                     self.parameters['B19TVUSpartpeakprice'] * lcu_usage_data['B19TVUSpartpeak_usage'] +
                     self.parameters['B19TVUSoffpeakprice'] * lcu_usage_data['B19TVUSoffpeak_usage'])
        B19TVUWprice = (self.parameters['B19TVUWpeakprice'] * lcu_usage_data['B19TVUWpeak_usage'] +
                      self.parameters['B19TVUWsuperoffpeakprice'] * lcu_usage_data['B19TVUWsuperoffpeak_usage'] +
                       self.parameters['B19TVUWoffpeakprice'] * lcu_usage_data['B19TVUWoffpeak_usage'])

        B19TVU_demand_charge= (self.parameters['B19TVUS_demand_rate'] * lcu_usage_data['Summer_highest_usage_B19TV']+self.parameters['B19TVUW_demand_rate'] * lcu_usage_data['Winter_highest_usage_B19TV'])

        B19TVUprice = B19TVUSprice + B19TVUWprice + (self.parameters['B19TVU_CCR'] * meter_input * time_in_use)+B19TVU_demand_charge

        B20SVUSprice = (self.parameters['B20SVUSpeakprice'] * lcu_usage_data['B20SVUSpeak_usage'] +
                     self.parameters['B20SVUSpartpeakprice'] * lcu_usage_data['B20SVUSpartpeak_usage'] +
                     self.parameters['B20SVUSoffpeakprice'] * lcu_usage_data['B20SVUSoffpeak_usage'])
        B20SVUWprice = (self.parameters['B20SVUWpeakprice'] * lcu_usage_data['B20SVUWpeak_usage'] +
                      self.parameters['B20SVUWsuperoffpeakprice'] * lcu_usage_data['B20SVUWsuperoffpeak_usage'] +
                       self.parameters['B20SVUWoffpeakprice'] * lcu_usage_data['B20SVUWoffpeak_usage'])

        B20SVU_demand_charge= (self.parameters['B20SVUS_demand_rate'] * lcu_usage_data['Summer_highest_usage_B20SV']+self.parameters['B20SVUW_demand_rate'] * lcu_usage_data['Winter_highest_usage_B20SV'])

        B20SVUprice = B20SVUSprice + B20SVUWprice + (self.parameters['B20SVU_CCR'] * meter_input * time_in_use)+B20SVU_demand_charge

        B20PVUSprice = (self.parameters['B20PVUSpeakprice'] * lcu_usage_data['B20PVUSpeak_usage'] +
                     self.parameters['B20PVUSpartpeakprice'] * lcu_usage_data['B20PVUSpartpeak_usage'] +
                     self.parameters['B20PVUSoffpeakprice'] * lcu_usage_data['B20PVUSoffpeak_usage'])
        B20PVUWprice = (self.parameters['B20PVUWpeakprice'] * lcu_usage_data['B20PVUWpeak_usage'] +
                      self.parameters['B20PVUWsuperoffpeakprice'] * lcu_usage_data['B20PVUWsuperoffpeak_usage'] +
                       self.parameters['B20PVUWoffpeakprice'] * lcu_usage_data['B20PVUWoffpeak_usage'])

        B20PVU_demand_charge= (self.parameters['B20PVUS_demand_rate'] * lcu_usage_data['Summer_highest_usage_B20PV']+self.parameters['B20PVUW_demand_rate'] * lcu_usage_data['Winter_highest_usage_B20PV'])
        B20PVUprice = B20PVUSprice + B20PVUWprice + (self.parameters['B20PVU_CCR'] * meter_input * time_in_use)+B20PVU_demand_charge

        B20TVUSprice = (self.parameters['B20TVUSpeakprice'] * lcu_usage_data['B20TVUSpeak_usage'] +
                     self.parameters['B20TVUSpartpeakprice'] * lcu_usage_data['B20TVUSpartpeak_usage'] +
                     self.parameters['B20TVUSoffpeakprice'] * lcu_usage_data['B20TVUSoffpeak_usage'])
        B20TVUWprice = (self.parameters['B20TVUWpeakprice'] * lcu_usage_data['B20TVUWpeak_usage'] +
                      self.parameters['B20TVUWsuperoffpeakprice'] * lcu_usage_data['B20TVUWsuperoffpeak_usage'] +
                       self.parameters['B20TVUWoffpeakprice'] * lcu_usage_data['B20TVUWoffpeak_usage'])

        B20TVU_demand_charge= (self.parameters['B20TVUS_demand_rate'] * lcu_usage_data['Summer_highest_usage_B20TV']+self.parameters['B20TVUW_demand_rate'] * lcu_usage_data['Winter_highest_usage_B20TV'])
        B20TVUprice = B20TVUSprice + B20TVUWprice + (self.parameters['B20TVU_CCR'] * meter_input * time_in_use)+B20TVU_demand_charge

        B19Uprice = B19SVUprice * B19SVU + B19PVUprice * B19PVU + B19TVUprice* B19TVU
        B20Uprice = B20SVUprice * B20SVU + B20PVUprice *B20PVU + B20TVUprice * B20TVU

        return(B19Uprice * B19U + B20Uprice * B20U)

    def optimize(self):
        objective = lambda x: self.objective(x)
        constraints = [
            {'type': 'eq', 'fun': lambda x: x[3] + x[7] - 1},
            {'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] - x[3]},
            {'type': 'eq', 'fun': lambda x: x[4] + x[5] + x[6] - x[7]},

        ]
        bounds = Bounds([0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1])
        x0_list = [1, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0],[0, 0, 1, 1, 0, 0, 0, 0],[0, 0, 0, 0, 1, 0, 0, 1],[0, 0, 0, 0, 0, 1, 0, 1],[0, 0, 0, 0, 0, 0, 1, 1]

        best_result = None

        for x0 in x0_list:
            result = minimize(objective, x0, method='SLSQP', constraints=constraints, bounds=bounds)
            x_opt = [round(xi) for xi in result.x]
            obj_val = self.objective(x_opt)

            if best_result is None or obj_val < best_result['objective']:
                best_result = {'x': x_opt, 'objective': obj_val}

        return best_result

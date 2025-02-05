# -*- coding: utf-8 -*-
"""smuelectricityrateplan.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Qkt0LPiJDfkgO62lJXqzmc96ETBPln7R
"""

# -*- coding: utf-8 -*-
"""SMU.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14OOX4teesLeIJUEjvWVqmxWS9q9FvIec
"""

from scipy.optimize import minimize
from scipy.optimize import Bounds
import pandas as pd

from components.electricity.sectors.smusector import SMUSector

class SMUElectricityRatePlan:
    def __init__(self, file_path, sheet_name, smu_usage_data):
        self.df = pd.read_excel(file_path, sheet_name=sheet_name)
        self.get_sum()
        self.parameters = {}
        self.smu_usage_data = smu_usage_data
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
        self.parameters['A1NTUS'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer', 'Non-TOU')
        self.parameters['A1NTUW'] = self.get_parameter('Small and Medium Business', 'A-1', 'Winter', 'Non-TOU')
        self.parameters['A1NTU_polyprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer','Non-TOU', phase='Poly', column='Customer Charge Rate')
        self.parameters['A1NTU_singleprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer','Non-TOU', phase='Single', column='Customer Charge Rate')
        self.parameters['A1USpeakprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer', 'Peak')
        self.parameters['A1USpartpeakprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer', 'Part-Peak')
        self.parameters['A1USoffpeakprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer', 'Off-Peak')
        self.parameters['A1UWpartpeakprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Winter', 'Part-Peak')
        self.parameters['A1UWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Winter', 'Off-Peak')
        self.parameters['A1U_polyprice'] = self.get_parameter('Small and Medium Business', 'A-1','Summer', 'Peak', phase='Poly', column='Customer Charge Rate')
        self.parameters['A1U_singleprice'] = self.get_parameter('Small and Medium Business', 'A-1', 'Summer','Peak', phase='Single', column='Customer Charge Rate')
        self.parameters['B1USpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Summer', 'Peak')
        self.parameters['B1USpartpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Summer', 'Part-Peak')
        self.parameters['B1USoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Summer', 'Off-Peak')
        self.parameters['B1UWpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Winter', 'Peak')
        self.parameters['B1UWsuperoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Winter', 'Super-Off-Peak')
        self.parameters['B1UWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Winter', 'Off-Peak')
        self.parameters['B1U_polyprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Summer','Peak', phase='Poly', column='Customer Charge Rate')
        self.parameters['B1U_singleprice'] = self.get_parameter('Small and Medium Business', 'B-1', 'Summer','Peak', phase='Single', column='Customer Charge Rate')
        self.parameters['B1STUSpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Summer', 'Peak')
        self.parameters['B1STUSpartpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Summer', 'Part-Peak')
        self.parameters['B1STUSoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Summer', 'Off-Peak')
        self.parameters['B1STUWpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Winter', 'Peak')
        self.parameters['B1STUWpartpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Winter', 'Part-Peak')
        self.parameters['B1STUWsuperoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Winter', 'Super-Off-Peak')
        self.parameters['B1STUWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST', 'Winter', 'Off-Peak')
        self.parameters['B1STU_polyprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST','Summer', 'Peak', phase='Poly', column='Customer Charge Rate')
        self.parameters['B1STU_singleprice'] = self.get_parameter('Small and Medium Business', 'B-1-ST','Summer', 'Peak', phase='Single', column='Customer Charge Rate')
        self.parameters['B1STU_demand_rate'] = 8.25
        self.parameters['B6USpeakprice'] = self.get_parameter('Small and Medium Business', 'B-6', 'Summer', 'Peak')
        self.parameters['B6USoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-6', 'Summer', 'Off-Peak')
        self.parameters['B6UWpeakprice'] = self.get_parameter('Small and Medium Business', 'B-6', 'Winter', 'Peak')
        self.parameters['B6UWsuperoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-6', 'Winter', 'Super-Off-Peak')
        self.parameters['B6UWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-6', 'Winter', 'Off-Peak')
        self.parameters['B6U_polyprice'] = self.get_parameter('Small and Medium Business', 'B-6','Summer', 'Peak', phase='Poly', column='Customer Charge Rate')
        self.parameters['B6U_singleprice'] = self.get_parameter('Small and Medium Business', 'B-6', 'Summer','Peak', phase='Single', column='Customer Charge Rate')
        self.parameters['B10SVUSpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Summer', 'Peak')
        self.parameters['B10SVUSpartpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Summer', 'Part-Peak')
        self.parameters['B10SVUSoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Summer', 'Off-Peak')
        self.parameters['B10SVUWpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Winter', 'Peak')
        self.parameters['B10SVUWsuperoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Winter', 'Super-Off-Peak')
        self.parameters['B10SVUWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Winter', 'Off-Peak')
        self.parameters['B10SVU_Customer_Charge'] = self.get_parameter('Small and Medium Business', 'B-10_SV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B10SVU_demand_rate'] = 21.87
        self.parameters['B10PVUSpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Summer', 'Peak')
        self.parameters['B10PVUSpartpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Summer', 'Part-Peak')
        self.parameters['B10PVUSoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Summer', 'Off-Peak')
        self.parameters['B10PVUWpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Winter', 'Peak')
        self.parameters['B10PVUWsuperoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Winter', 'Super-Off-Peak')
        self.parameters['B10PVUWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Winter', 'Off-Peak')
        self.parameters['B10PVU_Customer_Charge'] = self.get_parameter('Small and Medium Business', 'B-10_PV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B10PVU_demand_rate'] = 21.16
        self.parameters['B10TVUSpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Summer', 'Peak')
        self.parameters['B10TVUSpartpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Summer', 'Part-Peak')
        self.parameters['B10TVUSoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Summer', 'Off-Peak')
        self.parameters['B10TVUWpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Winter', 'Peak')
        self.parameters['B10TVUWsuperoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Winter', 'Super-Off-Peak')
        self.parameters['B10TVUWoffpeakprice'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Winter', 'Off-Peak')
        self.parameters['B10TVU_Customer_Charge'] = self.get_parameter('Small and Medium Business', 'B-10_TV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B10TVU_demand_rate'] = 14.46

    def objective(self, x):
        A1NTU, A1U, B1U, B1STU, B6U, B10SVU, B10PVU, B10TVU, A1NTU_poly, A1NTU_single, A1U_poly, A1U_single, B1U_poly, B1U_single, B1STU_poly, B1STU_single, B6U_poly, B6U_single = x
        smu_usage_data = self.smu_usage_data
        meter_input = smu_usage_data.meter_input
        time_in_use = smu_usage_data.time_in_use
        max_15min_usage = smu_usage_data.max_15min_usage
        B1STU_highest_demand_15mins = smu_usage_data.B1STU_highest_demand_15mins
        #meter_input, time_in_use, max_15min_usage, B1STU_highest_demand_15mins = smu_usage_data['meter_input'], smu_usage_data['time_in_use'], smu_usage_data['max_15min_usage'], smu_usage_data.B1STU_highest_demand_15mins

        A1NTUprice = (self.parameters['A1NTUS'] * smu_usage_data.A1NTUStotal_usage+
                      self.parameters['A1NTUW'] * smu_usage_data.A1NTUWtotal_usage +
                      (self.parameters['A1NTU_polyprice'] * A1NTU_poly + self.parameters['A1NTU_singleprice'] * A1NTU_single) * meter_input * time_in_use)
        A1USprice = (self.parameters['A1USpeakprice'] * smu_usage_data.A1USpeak_usage +
                     self.parameters['A1USpartpeakprice'] * smu_usage_data.A1USpartpeak_usage +
                     self.parameters['A1USoffpeakprice'] * smu_usage_data.A1USoffpeak_usage)
        A1UWprice = (self.parameters['A1UWpartpeakprice'] * smu_usage_data.A1UWpartpeak_usage +
                     self.parameters['A1UWoffpeakprice'] * smu_usage_data.A1UWoffpeak_usage)
        A1Uprice = A1USprice + A1UWprice + (self.parameters['A1U_polyprice'] * A1U_poly + self.parameters['A1U_singleprice'] * A1U_single) * meter_input * time_in_use

        B1USprice = (self.parameters['B1USpeakprice'] * smu_usage_data.B1USpeak_usage +
                     self.parameters['B1USpartpeakprice'] * smu_usage_data.B1USpartpeak_usage +
                     self.parameters['B1USoffpeakprice'] * smu_usage_data.B1USoffpeak_usage)
        B1UWprice = (self.parameters['B1UWpeakprice'] * smu_usage_data.B1UWpeak_usage +
                     self.parameters['B1UWsuperoffpeakprice'] * smu_usage_data.B1UWsuperoffpeak_usage +
                     self.parameters['B1UWoffpeakprice'] * smu_usage_data.B1UWoffpeak_usage)
        B1Uprice = B1USprice + B1UWprice + (self.parameters['B1U_polyprice'] * B1U_poly + self.parameters['B1U_singleprice'] * B1U_single) * meter_input * time_in_use

        B1STUSprice = (self.parameters['B1STUSpeakprice'] * smu_usage_data.B1STUSpeak_usage +
                       self.parameters['B1STUSpartpeakprice'] * smu_usage_data.B1STUSpartpeak_usage +
                       self.parameters['B1STUSoffpeakprice'] * smu_usage_data.B1STUSoffpeak_usage)
        B1STUWprice = (self.parameters['B1STUWpeakprice'] * smu_usage_data.B1STUWpeak_usage +
                       self.parameters['B1STUWpartpeakprice'] * smu_usage_data.B1STUWpartpeak_usage +
                       self.parameters['B1STUWsuperoffpeakprice'] * smu_usage_data.B1STUWsuperoffpeak_usage +
                       self.parameters['B1STUWoffpeakprice'] * smu_usage_data.B1STUWoffpeak_usage)
        B1STUprice = B1STUSprice + B1STUWprice + (self.parameters['B1STU_polyprice'] * B1STU_poly + self.parameters['B1STU_singleprice'] * B1STU_single) * meter_input * time_in_use + self.parameters['B1STU_demand_rate'] * B1STU_highest_demand_15mins

        B6USprice = (self.parameters['B6USpeakprice'] * smu_usage_data.B6USpeak_usage +
                     self.parameters['B6USoffpeakprice'] * smu_usage_data.B6USoffpeak_usage)
        B6UWprice = (self.parameters['B6UWpeakprice'] * smu_usage_data.B6UWpeak_usage+
                     self.parameters['B6UWsuperoffpeakprice'] * smu_usage_data.B6UWsuperoffpeak_usage +
                     self.parameters['B6UWoffpeakprice'] * smu_usage_data.B6UWoffpeak_usage)
        B6Uprice = B6USprice + B6UWprice + (self.parameters['B6U_polyprice'] * B6U_poly + self.parameters['B6U_singleprice'] * B6U_single) * meter_input * time_in_use

        B10SVUSprice = (self.parameters['B10SVUSpeakprice'] * smu_usage_data.B10SVUSpeak_usage +
                        self.parameters['B10SVUSpartpeakprice'] * smu_usage_data.B10SVUSpartpeak_usage +
                        self.parameters['B10SVUSoffpeakprice'] * smu_usage_data.B10SVUSoffpeak_usage)
        B10SVUWprice = (self.parameters['B10SVUWpeakprice'] * smu_usage_data.B10SVUWpeak_usage +
                        self.parameters['B10SVUWsuperoffpeakprice'] * smu_usage_data.B10SVUWsuperoffpeak_usage +
                        self.parameters['B10SVUWoffpeakprice'] * smu_usage_data.B10SVUWoffpeak_usage)
        B10SVUprice = B10SVUSprice + B10SVUWprice + self.parameters['B10SVU_Customer_Charge'] * meter_input * time_in_use + self.parameters['B10SVU_demand_rate'] * max_15min_usage

        B10PVUSprice = (self.parameters['B10PVUSpeakprice'] * smu_usage_data.B10PVUSpeak_usage +
                        self.parameters['B10PVUSpartpeakprice'] * smu_usage_data.B10PVUSpartpeak_usage +
                        self.parameters['B10PVUSoffpeakprice'] * smu_usage_data.B10PVUSoffpeak_usage)
        B10PVUWprice = (self.parameters['B10PVUWpeakprice'] * smu_usage_data.B10PVUWpeak_usage +
                        self.parameters['B10PVUWsuperoffpeakprice'] * smu_usage_data.B10PVUWsuperoffpeak_usage +
                        self.parameters['B10PVUWoffpeakprice'] * smu_usage_data.B10PVUWoffpeak_usage)
        B10PVUprice = B10PVUSprice + B10PVUWprice + self.parameters['B10PVU_Customer_Charge'] * meter_input * time_in_use + self.parameters['B10PVU_demand_rate'] * max_15min_usage

        B10TVUSprice = (self.parameters['B10TVUSpeakprice'] * smu_usage_data.B10TVUSpeak_usage +
                        self.parameters['B10TVUSpartpeakprice'] * smu_usage_data.B10TVUSpartpeak_usage +
                        self.parameters['B10TVUSoffpeakprice'] * smu_usage_data.B10TVUSoffpeak_usage)
        B10TVUWprice = (self.parameters['B10TVUWpeakprice'] * smu_usage_data.B10TVUWpeak_usage +
                        self.parameters['B10TVUWsuperoffpeakprice'] * smu_usage_data.B10TVUWsuperoffpeak_usage +
                        self.parameters['B10TVUWoffpeakprice'] * smu_usage_data.B10TVUWoffpeak_usage)
        B10TVUprice = B10TVUSprice + B10TVUWprice + self.parameters['B10TVU_Customer_Charge'] * meter_input * time_in_use + self.parameters['B10TVU_demand_rate'] * max_15min_usage

        return (A1NTUprice * A1NTU + A1Uprice * A1U + B1Uprice * B1U + B1STUprice * B1STU +
                B6Uprice * B6U + B10SVUprice * B10SVU + B10PVUprice * B10PVU + B10TVUprice * B10TVU)

    def optimize(self):
        objective = lambda x: self.objective(x)
        constraints = [
            {'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] - 1},
            {'type': 'eq', 'fun': lambda x: x[8] + x[9] - x[0]},  # A1NTB poly + single
            {'type': 'eq', 'fun': lambda x: x[10] + x[11] - x[1]},  # A1B poly + single
            {'type': 'eq', 'fun': lambda x: x[12] + x[13] - x[2]},  # B1B poly + single
            {'type': 'eq', 'fun': lambda x: x[14] + x[15] - x[3]},  # B1STB poly + single
            {'type': 'eq', 'fun': lambda x: x[16] + x[17] - x[4]},  # B6B poly + single
        ]
        bounds = Bounds([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        x0_list = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        best_result = None

        for x0 in x0_list:
            result = minimize(objective, x0, method='SLSQP', constraints=constraints, bounds=bounds)
            x_opt = [round(xi) for xi in result.x]
            obj_val = self.objective(x_opt)

            if best_result is None or obj_val < best_result['objective']:
                best_result = {'x': x_opt, 'objective': obj_val}
        
        return best_result

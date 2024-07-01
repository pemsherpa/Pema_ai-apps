# -*- coding: utf-8 -*-
"""lcbelectricityrateplan

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EVQ2csoDBigsI95JI6sdjzK7bgXIOTqn
"""

from scipy.optimize import minimize
from scipy.optimize import Bounds
import pandas as pd
import lcbsector.py
from sectors.lcbsector import LCBSector

class LCBElectricityRatePlan:
    def __init__(self, file_path, sheet_name, usage_data):
        self.df = pd.read_excel(file_path, sheet_name=sheet_name)
        self.usage_data = usage_data
        self.parameters = {}
        self.load_parameters()

    def get_parameter(self, sector, plan, season, ptype, phase=None, column='Energy Rate'):
        query = f"Sector == '{sector}' and Plan == '{plan}' and Season == '{season}' and Type == '{ptype}'"
        if phase:
            query += f" and Phase == '{phase}'"
        return self.df.query(query)[column].values[0]

    def load_parameters(self):
        # Load all required parameters
        self.parameters['B19SVBSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Peak')
        self.parameters['B19SVBSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Part-Peak')
        self.parameters['B19SVBSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Off-Peak')
        self.parameters['B19SVBWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Winter', 'Peak')
        self.parameters['B19SVBWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Winter', 'Super-Off-Peak')
        self.parameters['B19SVBWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Winter', 'Off-Peak')
        self.parameters['B19SVB_Customer_Charge'] = self.get_parameter('Large Commercial and Industrial', 'B-19_SV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B19SVB_demand_rate'] = 39.16
        self.parameters['B19PVBSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Peak')
        self.parameters['B19PVBSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Part-Peak')
        self.parameters['B19PVBSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Off-Peak')
        self.parameters['B19PVBWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Winter', 'Peak')
        self.parameters['B19PVBWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Winter', 'Super-Off-Peak')
        self.parameters['B19PVBWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Winter', 'Off-Peak')
        self.parameters['B19PVB_Customer_Charge'] = self.get_parameter('Large Commercial and Industrial', 'B-19_PV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B19PVB_demand_rate'] = 31.09
        self.parameters['B19TVBSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Peak')
        self.parameters['B19TVBSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Part-Peak')
        self.parameters['B19TVBSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Off-Peak')
        self.parameters['B19TVBWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Winter', 'Peak')
        self.parameters['B19TVBWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Winter', 'Super-Off-Peak')
        self.parameters['B19TVBWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Winter', 'Off-Peak')
        self.parameters['B19TVB_Customer_Charge'] = self.get_parameter('Large Commercial and Industrial', 'B-19_TV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B19TVB_demand_rate'] = 19.72
        self.parameters['B20SVBSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Peak')
        self.parameters['B20SVBSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Part-Peak')
        self.parameters['B20SVBSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Off-Peak')
        self.parameters['B20SVBWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Winter', 'Peak')
        self.parameters['B20SVBWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Winter', 'Super-Off-Peak')
        self.parameters['B20SVBWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Winter', 'Off-Peak')
        self.parameters['B20SVB_Customer_Charge'] = self.get_parameter('Large Commercial and Industrial', 'B-20_SV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B20SVB_demand_rate'] = 41.84
        self.parameters['B20PVBSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Peak')
        self.parameters['B20PVBSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Part-Peak')
        self.parameters['B20PVBSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Off-Peak')
        self.parameters['B20PVBWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Winter', 'Peak')
        self.parameters['B20PVBWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Winter', 'Super-Off-Peak')
        self.parameters['B20PVBWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Winter', 'Off-Peak')
        self.parameters['B20PVB_Customer_Charge'] = self.get_parameter('Large Commercial and Industrial', 'B-20_PV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B20PVB_demand_rate'] = 37.14
        self.parameters['B20TVBSpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Peak')
        self.parameters['B20TVBSpartpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Part-Peak')
        self.parameters['B20TVBSoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Off-Peak')
        self.parameters['B20TVBWpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Winter', 'Peak')
        self.parameters['B20TVBWsuperoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Winter', 'Super-Off-Peak')
        self.parameters['B20TVBWoffpeakprice'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Winter', 'Off-Peak')
        self.parameters['B20TVB_Customer_Charge'] = self.get_parameter('Large Commercial and Industrial', 'B-20_TV', 'Summer', 'Peak', column='Customer Charge Rate')
        self.parameters['B20TVB_demand_rate'] = 21.25

    def objective(self, x):
        B19SVB, B19PVB, B19TVB, B19B, B20SVB, B20PVB, B20TVB, B20B = x
        usage_data = self.usage_data
        meter_input, time_in_use, max_15min_usage = usage_data['meter_input'], usage_data['time_in_use'], usage_data['max_15min_usage']

        B19SVBSprice = (self.parameters['B19SVBSpeakprice'] * usage_data.B19SVBSpeak_usage +
                        self.parameters['B19SVBSpartpeakprice'] * usage_data.B19SVBSpartpeak_usage +
                        self.parameters['B19SVBSoffpeakprice'] * usage_data.B19SVBSoffpeak_usage)
        B19SVBWprice = (self.parameters['B19SVBWpeakprice'] * usage_data.B19SVBWpeak_usage +
                        self.parameters['B19SVBWsuperoffpeakprice'] * usage_data.B19SVBWsuperoffpeak_usage +
                        self.parameters['B19SVBWoffpeakprice'] * usage_data.B19SVBWoffpeak_usage)
        B19SVBprice = B19SVBSprice + B19SVBWprice + self.parameters['B19SVB_Customer_Charge'] * usage_data.meter_input * usage_data.time_in_use + self.parameters['B19SVB_demand_rate'] * usage_data.max_15min_usage

        B19PVBSprice = (self.parameters['B19PVBSpeakprice'] * usage_data.B19PVBSpeak_usage +
                        self.parameters['B19PVBSpartpeakprice'] * usage_data.B19PVBSpartpeak_usage +
                        self.parameters['B19PVBSoffpeakprice'] * usage_data.B19PVBSoffpeak_usage)
        B19PVBWprice = (self.parameters['B19PVBWpeakprice'] * usage_data.B19PVBWpeak_usage +
                        self.parameters['B19PVBWsuperoffpeakprice'] * usage_data.B19PVBWsuperoffpeak_usage +
                        self.parameters['B19PVBWoffpeakprice'] * usage_data.B19PVBWoffpeak_usage)
        B19PVBprice = B19PVBSprice + B19PVBWprice + self.parameters['B19PVB_Customer_Charge'] * usage_data.meter_input * usage_data.time_in_use + self.parameters['B19PVB_demand_rate'] * usage_data.max_15min_usage

        B19TVBSprice = (self.parameters['B19TVBSpeakprice'] * usage_data.B19TVBSpeak_usage +
                        self.parameters['B19TVBSpartpeakprice'] * usage_data.B19TVBSpartpeak_usage +
                        self.parameters['B19TVBSoffpeakprice'] * usage_data.B19TVBSoffpeak_usage)
        B19TVBWprice = (self.parameters['B19TVBWpeakprice'] * usage_data.B19TVBWpeak_usage +
                        self.parameters['B19TVBWsuperoffpeakprice'] * usage_data.B19TVBWsuperoffpeak_usage +
                        self.parameters['B19TVBWoffpeakprice'] * usage_data.B19TVBWoffpeak_usage)
        B19TVBprice = B19TVBSprice + B19TVBWprice + self.parameters['B19TVB_Customer_Charge'] * usage_data.meter_input * usage_data.time_in_use + self.parameters['B19TVB_demand_rate'] * usage_data.max_15min_usage

        B20SVBSprice = (self.parameters['B20SVBSpeakprice'] * usage_data.B20SVBSpeak_usage +
                        self.parameters['B20SVBSpartpeakprice'] * usage_data.B20SVBSpartpeak_usage +
                        self.parameters['B20SVBSoffpeakprice'] * usage_data.B20SVBSoffpeak_usage)
        B20SVBWprice = (self.parameters['B20SVBWpeakprice'] * usage_data.B20SVBWpeak_usage +
                        self.parameters['B20SVBWsuperoffpeakprice'] * usage_data.B20SVBWsuperoffpeak_usage +
                        self.parameters['B20SVBWoffpeakprice'] * usage_data.B20SVBWoffpeak_usage)
        B20SVBprice = B20SVBSprice + B20SVBWprice + self.parameters['B20SVB_Customer_Charge'] * usage_data.meter_input * usage_data.time_in_use + self.parameters['B20SVB_demand_rate'] * usage_data.max_15min_usage

        B20PVBSprice = (self.parameters['B20PVBSpeakprice'] * usage_data.B20PVBSpeak_usage +
                        self.parameters['B20PVBSpartpeakprice'] * usage_data.B20PVBSpartpeak_usage +
                        self.parameters['B20PVBSoffpeakprice'] * usage_data.B20PVBSoffpeak_usage)
        B20PVBWprice = (self.parameters['B20PVBWpeakprice'] * usage_data.B20PVBWpeak_usage +
                        self.parameters['B20PVBWsuperoffpeakprice'] * usage_data.B20PVBWsuperoffpeak_usage +
                        self.parameters['B20PVBWoffpeakprice'] * usage_data.B20PVBWoffpeak_usage)
        B20PVBprice = B20PVBSprice + B20PVBWprice + self.parameters['B20PVB_Customer_Charge'] * usage_data.meter_input * usage_data.time_in_use + self.parameters['B20PVB_demand_rate'] * usage_data.max_15min_usage

        B20TVBSprice = (self.parameters['B20TVBSpeakprice'] * usage_data.B20TVBSpeak_usage +
                        self.parameters['B20TVBSpartpeakprice'] * usage_data.B20TVBSpartpeak_usage +
                        self.parameters['B20TVBSoffpeakprice'] * usage_data.B20TVBSoffpeak_usage)
        B20TVBWprice = (self.parameters['B20TVBWpeakprice'] * usage_data.B20TVBWpeak_usage +
                        self.parameters['B20TVBWsuperoffpeakprice'] * usage_data.B20TVBWsuperoffpeak_usage +
                        self.parameters['B20TVBWoffpeakprice'] * usage_data.B20TVBWoffpeak_usage)
        B20TVBprice = B20TVBSprice + B20TVBWprice + self.parameters['B20TVB_Customer_Charge'] * usage_data.meter_input * usage_data.time_in_use + self.parameters['B20TVB_demand_rate'] * usage_data.max_15min_usage

        return (B19SVBprice * B19SVB + B19PVBprice * B19PVB + B19TVBprice * B19TVB + B20SVBprice * B20SVB + B20PVBprice * B20PVB + B20TVBprice * B20TVB)

    def optimize(self):
     objective = lambda x: self.objective(x)
     constraints = [
        {'type': 'eq', 'fun': lambda x: x[3] + x[7] - 1},
        {'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] - x[3]},
        {'type': 'eq', 'fun': lambda x: x[4] + x[5] + x[6] - x[7]},
     ]
     bounds = Bounds([0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1])
     x0 = [0, 0, 0, 0, 1, 0, 0, 1]

     result = minimize(objective, x0, method='SLSQP', constraints=constraints, bounds=bounds)

    # Round results to enforce binary constraints
     x_opt = [round(xi) for xi in result.x]
     obj_val = self.objective(x_opt)

     return {'x': x_opt, 'objective': obj_val}
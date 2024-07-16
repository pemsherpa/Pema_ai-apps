class LCBSector:        
    def __init__(self, B19SVBSpeak_usage, B19SVBSpartpeak_usage, B19SVBSoffpeak_usage,
                 B19SVBWpeak_usage,B19SVBWsuperoffpeak_usage,B19SVBWoffpeak_usage,
                 B19PVBSpeak_usage,B19PVBSpartpeak_usage,B19PVBSoffpeak_usage,
                 B19PVBWpeak_usage,B19PVBWsuperoffpeak_usage,B19PVBWoffpeak_usage,
                 B19TVBSpeak_usage,B19TVBSpartpeak_usage,B19TVBSoffpeak_usage,
                 B19TVBWpeak_usage,B19TVBWsuperoffpeak_usage,B19TVBWoffpeak_usage,
                 B20SVBSpeak_usage, B20SVBSpartpeak_usage, B20SVBSoffpeak_usage,
                 B20SVBWpeak_usage,B20SVBWsuperoffpeak_usage,B20SVBWoffpeak_usage,
                 B20PVBSpeak_usage,B20PVBSpartpeak_usage,B20PVBSoffpeak_usage,
                 B20PVBWpeak_usage,B20PVBWsuperoffpeak_usage,B20PVBWoffpeak_usage,
                 B20TVBSpeak_usage,B20TVBSpartpeak_usage,B20TVBSoffpeak_usage,
                 B20TVBWpeak_usage,B20TVBWsuperoffpeak_usage,B20TVBWoffpeak_usage,
                 meter_input,time_in_use,max_15min_usage):
        self.B19SVBSpeak_usage = B19SVBSpeak_usage
        self.B19SVBSpartpeak_usage = B19SVBSpartpeak_usage
        self.B19SVBSoffpeak_usage = B19SVBSoffpeak_usage
        self.B19SVBWpeak_usage = B19SVBWpeak_usage
        self.B19SVBWsuperoffpeak_usage = B19SVBWsuperoffpeak_usage
        self.B19SVBWoffpeak_usage = B19SVBWoffpeak_usage
        self.B19PVBSpeak_usage = B19PVBSpeak_usage
        self.B19PVBSpartpeak_usage = B19PVBSpartpeak_usage
        self.B19PVBSoffpeak_usage = B19PVBSoffpeak_usage
        self.B19PVBWpeak_usage = B19PVBWpeak_usage
        self.B19PVBWsuperoffpeak_usage = B19PVBWsuperoffpeak_usage
        self.B19PVBWoffpeak_usage = B19PVBWoffpeak_usage
        self.B19TVBSpeak_usage = B19TVBSpeak_usage
        self.B19TVBSpartpeak_usage = B19TVBSpartpeak_usage
        self.B19TVBSoffpeak_usage = B19TVBSoffpeak_usage
        self.B19TVBWpeak_usage = B19TVBWpeak_usage
        self.B19TVBWsuperoffpeak_usage = B19TVBWsuperoffpeak_usage
        self.B19TVBWoffpeak_usage = B19TVBWoffpeak_usage
        self.B20SVBSpeak_usage = B20SVBSpeak_usage
        self.B20SVBSpartpeak_usage = B20SVBSpartpeak_usage
        self.B20SVBSoffpeak_usage = B20SVBSoffpeak_usage
        self.B20SVBWpeak_usage = B20SVBWpeak_usage
        self.B20SVBWsuperoffpeak_usage = B20SVBWsuperoffpeak_usage
        self.B20SVBWoffpeak_usage = B20SVBWoffpeak_usage
        self.B20PVBSpeak_usage = B20PVBSpeak_usage
        self.B20PVBSpartpeak_usage = B20PVBSpartpeak_usage
        self.B20PVBSoffpeak_usage = B20PVBSoffpeak_usage
        self.B20PVBWpeak_usage = B20PVBWpeak_usage
        self.B20PVBWsuperoffpeak_usage = B20PVBWsuperoffpeak_usage
        self.B20PVBWoffpeak_usage = B20PVBWoffpeak_usage
        self.B20TVBSpeak_usage = B20TVBSpeak_usage
        self.B20TVBSpartpeak_usage = B20TVBSpartpeak_usage
        self.B20TVBSoffpeak_usage = B20TVBSoffpeak_usage
        self.B20TVBWpeak_usage = B20TVBWpeak_usage
        self.B20TVBWsuperoffpeak_usage = B20TVBWsuperoffpeak_usage
        self.B20TVBWoffpeak_usage = B20TVBWoffpeak_usage
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
class LCBSector_simplified:        
    def calculate_hours(self, start_time, stop_time):
        if start_time == 'Other' or stop_time == 'Other':
            return 0
        else:
            start_hour = start_time.hour
            stop_hour = stop_time.hour
            hours= stop_hour - start_hour
            return hours
                
    def __init__(self, user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage, user_electricity_bill_season,
                 meter_input,time_in_use,max_15min_usage, user_sector,user_current_plan):
        import pandas as pd
        Bundled_peak_time_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Bundled Peak Time Price')
        
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
        self.user_input_peak_usage = user_input_peak_usage
        self.user_input_part_peak_usage = user_input_part_peak_usage
        self.user_input_super_off_peak_usage = user_input_super_off_peak_usage
        self.user_input_off_peak_usage = user_input_off_peak_usage
        self.user_electricity_bill_season = user_electricity_bill_season
        self.user_sector = user_sector
        self.user_current_plan = user_current_plan

        if user_electricity_bill_season == 'Summer':
            summer_peak_usage = user_input_peak_usage
            summer_part_peak_usage = user_input_part_peak_usage
            summer_off_peak_usage = user_input_off_peak_usage

            peak_df = Bundled_peak_time_df[(Bundled_peak_time_df['Sector'] == user_sector) & (Bundled_peak_time_df['Plan'] == user_current_plan) &(Bundled_peak_time_df['Type']=='Peak')&(Bundled_peak_time_df['Season']=='Summer')]
            part_peak_df = Bundled_peak_time_df[(Bundled_peak_time_df['Sector'] == user_sector) & (Bundled_peak_time_df['Plan'] == user_current_plan) &(Bundled_peak_time_df['Type']=='Part-Peak')& (Bundled_peak_time_df['Season']=='Summer')]
            off_peak_df = Bundled_peak_time_df[(Bundled_peak_time_df['Sector'] == user_sector) & (Bundled_peak_time_df['Plan'] == user_current_plan) &(Bundled_peak_time_df['Type']=='Off-Peak')&(Bundled_peak_time_df['Season']=='Summer')]

            start_time_peak = peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
            stop_time_peak = peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
            summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)


            start_time_part_peak=part_peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
            stop_time_part_peak=part_peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
            summer_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)

            start_time_off_peak=off_peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
            stop_time_off_peak=off_peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
            summer_off_peak_time_hours= 24 - summer_peak_time_hours - summer_part_peak_time_hours

            self.B19SVBSpeak_usage = summer_peak_usage
            self.B19PVBSpeak_usage = summer_peak_usage
            self.B19TVBSpeak_usage = summer_peak_usage
            self.B19SVBSpartpeak_usage = summer_part_peak_usage
            self.B19PVBSpartpeak_usage = summer_part_peak_usage
            self.B19TVBSpartpeak_usage = summer_part_peak_usage
            self.B19SVBSoffpeak_usage = summer_off_peak_usage
            self.B19PVBSoffpeak_usage = summer_off_peak_usage
            self.B19TVBSoffpeak_usage = summer_off_peak_usage

            self.B20SVBSpeak_usage = summer_peak_usage
            self.B20PVBSpeak_usage = summer_peak_usage
            self.B20TVBSpeak_usage = summer_peak_usage
            self.B20SVBSpartpeak_usage = summer_part_peak_usage
            self.B20PVBSpartpeak_usage = summer_part_peak_usage
            self.B20TVBSpartpeak_usage = summer_part_peak_usage
            self.B20SVBSoffpeak_usage = summer_off_peak_usage
            self.B20PVBSoffpeak_usage = summer_off_peak_usage
            self.B20TVBSoffpeak_usage = summer_off_peak_usage

            usage_dict = {}
            for hour in range(24):
                if hour in range(16, 21):
                    usage_dict[f'{hour}_oclock_usage'] = summer_peak_usage / summer_peak_time_hours
                elif hour in range(14, 16) or hour in range(21, 23):
                    usage_dict[f'{hour}_oclock_usage'] = summer_part_peak_usage / summer_part_peak_time_hours
                else:
                    usage_dict[f'{hour}_oclock_usage'] = summer_off_peak_usage / summer_off_peak_time_hours

            self.B19SVBWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
            self.B19SVBWsuperoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9, 14)])
            self.B19SVBWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

            self.B19PVBWpeak_usage = self.B19SVBWpeak_usage
            self.B19PVBWsuperoffpeak_usage = self.B19SVBWsuperoffpeak_usage
            self.B19PVBWoffpeak_usage = self.B19SVBWoffpeak_usage
            self.B19TVBWpeak_usage = self.B19SVBWpeak_usage
            self.B19TVBWsuperoffpeak_usage = self.B19SVBWsuperoffpeak_usage
            self.B19TVBWoffpeak_usage = self.B19SVBWoffpeak_usage
            self.B20SVBWpeak_usage = self.B19SVBWpeak_usage
            self.B20SVBWsuperoffpeak_usage = self.B19SVBWsuperoffpeak_usage
            self.B20SVBWoffpeak_usage = self.B19SVBWoffpeak_usage
            self.B20PVBWpeak_usage = self.B19SVBWpeak_usage
            self.B20PVBWsuperoffpeak_usage = self.B19SVBWsuperoffpeak_usage
            self.B20PVBWoffpeak_usage = self.B19SVBWoffpeak_usage
            self.B20TVBWpeak_usage = self.B19SVBWpeak_usage
            self.B20TVBWsuperoffpeak_usage = self.B19SVBWsuperoffpeak_usage
            self.B20TVBWoffpeak_usage = self.B19SVBWoffpeak_usage

        elif user_electricity_bill_season == 'Winter':
            winter_peak_usage = user_input_peak_usage
            winter_off_peak_usage = user_input_off_peak_usage
            winter_super_off_peak_usage = user_input_super_off_peak_usage

            peak_df = Bundled_peak_time_df[(Bundled_peak_time_df['Sector'] == user_sector) & (Bundled_peak_time_df['Plan'] == user_current_plan) &(Bundled_peak_time_df['Type']=='Peak')&(Bundled_peak_time_df['Season']=='Winter')]
            super_off_peak_df = Bundled_peak_time_df[(Bundled_peak_time_df['Sector'] == user_sector) & (Bundled_peak_time_df['Plan'] == user_current_plan) &(Bundled_peak_time_df['Type']=='Super-Off-Peak')& (Bundled_peak_time_df['Season']=='Winter')]
            off_peak_df = Bundled_peak_time_df[(Bundled_peak_time_df['Sector'] == user_sector) & (Bundled_peak_time_df['Plan'] == user_current_plan) &(Bundled_peak_time_df['Type']=='Off-Peak')&(Bundled_peak_time_df['Season']=='Winter')]
                
            start_time_peak = peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
            stop_time_peak = peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
            winter_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)


            start_time_super_off_peak=super_off_peak_df['Peak Start Time'].iloc[0] if not super_off_peak_df['Peak Start Time'].empty else 'Other'
            stop_time_super_off_peak=super_off_peak_df['Peak End Time'].iloc[0] if not super_off_peak_df['Peak End Time'].empty else 'Other'
            winter_super_off_peak_time_hours=self.calculate_hours(start_time_super_off_peak,stop_time_super_off_peak)

            start_time_off_peak=off_peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
            stop_time_off_peak=off_peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
            winter_off_peak_time_hours= 24 - winter_peak_time_hours - winter_super_off_peak_time_hours

            self.B19SVBWpeak_usage = winter_peak_usage
            self.B19PVBWpeak_usage = winter_peak_usage
            self.B19TVBWpeak_usage = winter_peak_usage
            self.B19SVBWsuperoff_usage = winter_super_off_peak_usage
            self.B19PVBWsuperoff_usage = winter_super_off_peak_usage
            self.B19TVBWsuperoff_usage = winter_super_off_peak_usage
            self.B19SVBWoffpeak_usage = winter_off_peak_usage
            self.B19PVBWoffpeak_usage = winter_off_peak_usage
            self.B19TVBWoffpeak_usage = winter_off_peak_usage

            self.B20SVBWpeak_usage = winter_peak_usage
            self.B20PVBWpeak_usage = winter_peak_usage
            self.B20TVBWpeak_usage = winter_peak_usage
            self.B20SVBWsuperoff_peak_usage = winter_super_off_peak_usage
            self.B20PVBWsuperoff_peak_usage = winter_super_off_peak_usage
            self.B20TVBWsuperoffpeak_usage = winter_super_off_peak_usage
            self.B20SVBWoffpeak_usage = winter_off_peak_usage
            self.B20PVBWoffpeak_usage = winter_off_peak_usage
            self.B20TVBWoffpeak_usage = winter_off_peak_usage

            usage_dict = {}
            for hour in range(24):
                if hour in range(16, 21):
                    usage_dict[f'{hour}_oclock_usage'] = winter_peak_usage / winter_peak_time_hours
                elif hour in range(9, 14):
                    usage_dict[f'{hour}_oclock_usage'] = winter_super_off_peak_usage / winter_super_off_peak_time_hours
                else:
                    usage_dict[f'{hour}_oclock_usage'] = winter_off_peak_usage / winter_off_peak_time_hours

            self.B19SVBSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
            self.B19SVBSpart_peak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])
            self.B19SVBSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

            self.B19PVBSpeak_usage = self.B19SVBSpeak_usage
            self.B19PVBSpartpeak_usage = self.B19SVBSpart_peak_usage
            self.B19PVBSoffpeak_usage = self.B19SVBSoffpeak_usage
            self.B19TVBSpeak_usage = self.B19SVBSpeak_usage
            self.B19TVBSpartpeak_usage = self.B19SVBSpart_peak_usage
            self.B19TVBSoffpeak_usage = self.B19SVBSoffpeak_usage
            self.B20SVBSpeak_usage = self.B19SVBSpeak_usage
            self.B20SVBSpartpeak_usage = self.B19SVBSpart_peak_usage
            self.B20SVBSoffpeak_usage = self.B19SVBSoffpeak_usage
            self.B20PVBSpeak_usage = self.B19SVBSpeak_usage
            self.B20PVBSpartpeak_usage = self.B19SVBSpart_peak_usage
            self.B20PVBSoffpeak_usage = self.B19SVBSoffpeak_usage
            self.B20TVBSpeak_usage = self.B19SVBSpeak_usage
            self.B20TVBSpartpeak_usage = self.B19SVBSpart_peak_usage
            self.B20TVBSoffpeak_usage = self.B19SVBSoffpeak_usage
        else:
            result = 0


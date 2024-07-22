from components.electricity.sectors.sector_simplified import ElectricUsage, Sector_simplified
import pandas as pd

class LCUSector:
    def __init__(self, B19SVUSpeak_usage, B19SVUSpartpeak_usage, B19SVUSoffpeak_usage,
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
        self.B19SVUSpeak_usage = B19SVUSpeak_usage
        self.B19SVUSpartpeak_usage = B19SVUSpartpeak_usage
        self.B19SVUSoffpeak_usage = B19SVUSoffpeak_usage
        self.B19SVUWpeak_usage = B19SVUWpeak_usage
        self.B19SVUWsuperoffpeak_usage = B19SVUWsuperoffpeak_usage
        self.B19SVUWoffpeak_usage = B19SVUWoffpeak_usage
        self.Summer_highest_usage_B19SV = Summer_highest_usage_B19SV
        self.Winter_highest_usage_B19SV = Winter_highest_usage_B19SV
        self.B19PVUSpeak_usage = B19PVUSpeak_usage
        self.B19PVUSpartpeak_usage = B19PVUSpartpeak_usage
        self.B19PVUSoffpeak_usage = B19PVUSoffpeak_usage
        self.B19PVUWpeak_usage = B19PVUWpeak_usage
        self.B19PVUWsuperoffpeak_usage = B19PVUWsuperoffpeak_usage
        self.B19PVUWoffpeak_usage = B19PVUWoffpeak_usage
        self.Summer_highest_usage_B19PV = Summer_highest_usage_B19PV
        self.Winter_highest_usage_B19PV = Winter_highest_usage_B19PV
        self.B19TVUSpeak_usage = B19TVUSpeak_usage
        self.B19TVUSpartpeak_usage = B19TVUSpartpeak_usage
        self.B19TVUSoffpeak_usage = B19TVUSoffpeak_usage
        self.B19TVUWpeak_usage = B19TVUWpeak_usage
        self.B19TVUWsuperoffpeak_usage = B19TVUWsuperoffpeak_usage
        self.B19TVUWoffpeak_usage = B19TVUWoffpeak_usage
        self.Summer_highest_usage_B19TV = Summer_highest_usage_B19TV
        self.Winter_highest_usage_B19TV = Winter_highest_usage_B19TV
        self.B20SVUSpeak_usage = B20SVUSpeak_usage
        self.B20SVUSpartpeak_usage = B20SVUSpartpeak_usage
        self.B20SVUSoffpeak_usage = B20SVUSoffpeak_usage
        self.B20SVUWpeak_usage = B20SVUWpeak_usage
        self.B20SVUWsuperoffpeak_usage = B20SVUWsuperoffpeak_usage
        self.B20SVUWoffpeak_usage = B20SVUWoffpeak_usage
        self.Summer_highest_usage_B20SV = Summer_highest_usage_B20SV
        self.Winter_highest_usage_B20SV = Winter_highest_usage_B20SV
        self.B20PVUSpeak_usage = B20PVUSpeak_usage
        self.B20PVUSpartpeak_usage = B20PVUSpartpeak_usage
        self.B20PVUSoffpeak_usage = B20PVUSoffpeak_usage
        self.B20PVUWpeak_usage = B20PVUWpeak_usage
        self.B20PVUWsuperoffpeak_usage = B20PVUWsuperoffpeak_usage
        self.B20PVUWoffpeak_usage = B20PVUWoffpeak_usage
        self.Summer_highest_usage_B20PV = Summer_highest_usage_B20PV
        self.Winter_highest_usage_B20PV = Winter_highest_usage_B20PV
        self.B20TVUSpeak_usage = B20TVUSpeak_usage
        self.B20TVUSpartpeak_usage = B20TVUSpartpeak_usage
        self.B20TVUSoffpeak_usage = B20TVUSoffpeak_usage
        self.B20TVUWpeak_usage = B20TVUWpeak_usage
        self.B20TVUWsuperoffpeak_usage = B20TVUWsuperoffpeak_usage
        self.B20TVUWoffpeak_usage = B20TVUWoffpeak_usage
        self.Summer_highest_usage_B20TV = Summer_highest_usage_B20TV
        self.Winter_highest_usage_B20TV = Winter_highest_usage_B20TV
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage

class LCUSector_simplified(Sector_simplified):
    def calculate_hours(self, start_time, stop_time):
        if start_time == 'Other' or stop_time == 'Other':
            return 0
        else:
            start_hour = start_time.hour
            stop_hour = stop_time.hour
            hours= stop_hour - start_hour
            return hours

    def __init__(self, user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage, user_electricity_bill_season,
                 meter_input,time_in_use,max_15min_usage, user_sector,user_current_plan,kwh_used):
        super().__init__()
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
        self.kwh_used=kwh_used

        if user_current_plan in ('B-19_S','B-20_S','B-20_P'):
            return kwh_used

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

            self.B19SVUSpeak_usage = summer_peak_usage
            self.B19PVUSpeak_usage = summer_peak_usage
            self.B19TVUSpeak_usage = summer_peak_usage
            self.B19SVUSpartpeak_usage = summer_part_peak_usage
            self.B19PVUSpartpeak_usage = summer_part_peak_usage
            self.B19TVUSpartpeak_usage = summer_part_peak_usage
            self.B19SVUSoffpeak_usage = summer_off_peak_usage
            self.B19PVUSoffpeak_usage = summer_off_peak_usage
            self.B19TVUSoffpeak_usage = summer_off_peak_usage

            self.B20SVUSpeak_usage = summer_peak_usage
            self.B20PVUSpeak_usage = summer_peak_usage
            self.B20TVUSpeak_usage = summer_peak_usage
            self.B20SVUSpartpeak_usage = summer_part_peak_usage
            self.B20PVUSpartpeak_usage = summer_part_peak_usage
            self.B20TVUSpartpeak_usage = summer_part_peak_usage
            self.B20SVUSoffpeak_usage = summer_off_peak_usage
            self.B20PVUSoffpeak_usage = summer_off_peak_usage
            self.B20TVUSoffpeak_usage = summer_off_peak_usage

            peak_range = list(range(16, 21))
            part_peak_range = list(range(14, 16)) + list(range(21, 23))
            peak_usage = ElectricUsage(summer_peak_usage, summer_peak_time_hours)
            part_peak_usage = ElectricUsage(summer_part_peak_usage, summer_part_peak_time_hours)
            off_peak_usage = ElectricUsage(summer_off_peak_usage, summer_off_peak_usage)
            usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)

            self.B19SVUWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
            self.B19SVUWsuperoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9, 14)])
            self.B19SVUWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

            self.B19PVUWpeak_usage = self.B19SVUWpeak_usage
            self.B19PVUWsuperoffpeak_usage = self.B19SVUWsuperoffpeak_usage
            self.B19PVUWoffpeak_usage = self.B19SVUWoffpeak_usage
            self.B19TVUWpeak_usage = self.B19SVUWpeak_usage
            self.B19TVUWsuperoffpeak_usage = self.B19SVUWsuperoffpeak_usage
            self.B19TVUWoffpeak_usage = self.B19SVUWoffpeak_usage
            self.B20SVUWpeak_usage = self.B19SVUWpeak_usage
            self.B20SVUWsuperoffpeak_usage = self.B19SVUWsuperoffpeak_usage
            self.B20SVUWoffpeak_usage = self.B19SVUWoffpeak_usage
            self.B20PVUWpeak_usage = self.B19SVUWpeak_usage
            self.B20PVUWsuperoffpeak_usage = self.B19SVUWsuperoffpeak_usage
            self.B20PVUWoffpeak_usage = self.B19SVUWoffpeak_usage
            self.B20TVUWpeak_usage = self.B19SVUWpeak_usage
            self.B20TVUWsuperoffpeak_usage = self.B19SVUWsuperoffpeak_usage
            self.B20TVUWoffpeak_usage = self.B19SVUWoffpeak_usage
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

            self.B19SVUWpeak_usage = winter_peak_usage
            self.B19PVUWpeak_usage = winter_peak_usage
            self.B19TVUWpeak_usage = winter_peak_usage
            self.B19SVUWsuperoff_usage = winter_super_off_peak_usage
            self.B19PVUWsuperoff_usage = winter_super_off_peak_usage
            self.B19TVUWsuperoff_usage = winter_super_off_peak_usage
            self.B19SVUWoffpeak_usage = winter_off_peak_usage
            self.B19PVUWoffpeak_usage = winter_off_peak_usage
            self.B19TVUWoffpeak_usage = winter_off_peak_usage

            self.B20SVUWpeak_usage = winter_peak_usage
            self.B20PVUWpeak_usage = winter_peak_usage
            self.B20TVUWpeak_usage = winter_peak_usage
            self.B20SVUWsuperoff_peak_usage = winter_super_off_peak_usage
            self.B20PVUWsuperoff_peak_usage = winter_super_off_peak_usage
            self.B20TVUWsuperoffpeak_usage = winter_super_off_peak_usage
            self.B20SVUWoffpeak_usage = winter_off_peak_usage
            self.B20PVUWoffpeak_usage = winter_off_peak_usage
            self.B20TVUWoffpeak_usage = winter_off_peak_usage
            
            peak_range = list(range(16, 21))
            part_peak_range = list(range(9, 14))
            peak_usage = ElectricUsage(winter_peak_usage, winter_peak_time_hours)
            part_peak_usage = ElectricUsage(winter_super_off_peak_usage, winter_super_off_peak_time_hours)
            off_peak_usage = ElectricUsage(winter_off_peak_usage, winter_off_peak_time_hours)
            usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)

            self.B19SVUSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
            self.B19SVUSpart_peak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])
            self.B19SVUSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

            self.B19PVUSpeak_usage = self.B19SVUSpeak_usage
            self.B19PVUSpartpeak_usage = self.B19SVUSpart_peak_usage
            self.B19PVUSoffpeak_usage = self.B19SVUSoffpeak_usage
            self.B19TVUSpeak_usage = self.B19SVUSpeak_usage
            self.B19TVUSpartpeak_usage = self.B19SVUSpart_peak_usage
            self.B19TVUSoffpeak_usage = self.B19SVUSoffpeak_usage
            self.B20SVUSpeak_usage = self.B19SVUSpeak_usage
            self.B20SVUSpartpeak_usage = self.B19SVUSpart_peak_usage
            self.B20SVUSoffpeak_usage = self.B19SVUSoffpeak_usage
            self.B20PVUSpeak_usage = self.B19SVUSpeak_usage
            self.B20PVUSpartpeak_usage = self.B19SVUSpart_peak_usage
            self.B20PVUSoffpeak_usage = self.B19SVUSoffpeak_usage
            self.B20TVUSpeak_usage = self.B19SVUSpeak_usage
            self.B20TVUSpartpeak_usage = self.B19SVUSpart_peak_usage
            self.B20TVUSoffpeak_usage = self.B19SVUSoffpeak_usage
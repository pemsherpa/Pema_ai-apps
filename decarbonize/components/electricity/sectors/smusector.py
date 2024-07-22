
import pandas as pd

from components.electricity.sectors.sector_simplified import Sector_simplified

class SMUSector:
    def __init__(self, A1NTUStotal_usage, A1NTUWtotal_usage, A1USpeak_usage,
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
        self.A1NTUStotal_usage = A1NTUStotal_usage
        self.A1NTUWtotal_usage = A1NTUWtotal_usage
        self.A1USpeak_usage = A1USpeak_usage
        self.A1USpartpeak_usage = A1USpartpeak_usage
        self.A1USoffpeak_usage = A1USoffpeak_usage
        self.A1UWpartpeak_usage = A1UWpartpeak_usage
        self.A1UWoffpeak_usage = A1UWoffpeak_usage
        self.B1USpeak_usage = B1USpeak_usage
        self.B1USpartpeak_usage = B1USpartpeak_usage
        self.B1USoffpeak_usage = B1USoffpeak_usage
        self.B1UWpeak_usage = B1UWpeak_usage
        self.B1UWsuperoffpeak_usage = B1UWsuperoffpeak_usage
        self.B1UWoffpeak_usage = B1UWoffpeak_usage
        self.B1UTBSpeak_usage = B1STUSpeak_usage
        self.B1STUSpartpeak_usage = B1STUSpartpeak_usage
        self.B1STUSoffpeak_usage = B1STUSoffpeak_usage
        self.B1STUWpeak_usage = B1STUWpeak_usage
        self.B1STUWpartpeak_usage = B1STUWpartpeak_usage
        self.B1STUWsuperoffpeak_usage = B1STUWsuperoffpeak_usage
        self.B1STUWoffpeak_usage = B1STUWoffpeak_usage
        self.B6USpeak_usage = B6USpeak_usage
        self.B6USoffpeak_usage = B6USoffpeak_usage
        self.B6UWpeak_usage = B6UWpeak_usage
        self.B6UWsuperoffpeak_usage = B6UWsuperoffpeak_usage
        self.B6UWoffpeak_usage = B6UWoffpeak_usage
        self.B10SVUSpeak_usage = B10SVUSpeak_usage
        self.B10SVUSpartpeak_usage = B10SVUSpartpeak_usage
        self.B10SVUSoffpeak_usage = B10SVUSoffpeak_usage
        self.B10SVUWpeak_usage = B10SVUWpeak_usage
        self.B10SVUWsuperoffpeak_usage = B10SVUWsuperoffpeak_usage
        self.B10SVUWoffpeak_usage = B10SVUWoffpeak_usage
        self.B10PVUSpeak_usage = B10PVUSpeak_usage
        self.B10PVUSpartpeak_usage = B10PVUSpartpeak_usage
        self.B10PVUSoffpeak_usage = B10PVUSoffpeak_usage
        self.B10PVUWpeak_usage = B10PVUWpeak_usage
        self.B10PVUWsuperoffpeak_usage = B10PVUWsuperoffpeak_usage
        self.B10PVUWoffpeak_usage = B10PVUWoffpeak_usage
        self.B10TVUSpeak_usage = B10TVUSpeak_usage
        self.B10TVUSpartpeak_usage = B10TVUSpartpeak_usage
        self.B10TVUSoffpeak_usage = B10TVUSoffpeak_usage
        self.B10TVUWpeak_usage = B10TVUWpeak_usage
        self.B10TVUWsuperoffpeak_usage = B10TVUWsuperoffpeak_usage
        self.B10TVUWoffpeak_usage = B10TVUWoffpeak_usage
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
        self.B1STU_highest_demand_15mins = B1STU_highest_demand_15mins

class SMUSector_simplified(Sector_simplified):
   def calculate_hours(self,start_time, stop_time):
          if start_time == 'Other' or stop_time == 'Other':
            return 0
          else:
            start_hour = start_time.hour
            stop_hour = stop_time.hour
            hours= stop_hour - start_hour
            return hours

   def __init__(self, user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage,meter_input,time_in_use,max_15min_usage, user_sector,user_B1STU_highest_demand_15mins,kwh_used):
        if(user_input_peak_usage<=23 or user_input_part_peak_usage<=23 or user_input_super_off_peak_usage<=23 or user_input_off_peak_usage<=23):
            raise ValueError('Minimum Peak usage not met,should be greater than 23')
        super().__init__()

        self.Bundled_peak_time_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Unbundled Peak Time Price')

        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
        self.kwh_used = kwh_used
        self.user_input_peak_usage = user_input_peak_usage
        self.user_input_part_peak_usage = user_input_part_peak_usage
        self.user_input_super_off_peak_usage = user_input_super_off_peak_usage
        self.user_input_off_peak_usage = user_input_off_peak_usage
        self.user_sector = user_sector
        self.seasons=['Winter','Summer']
        self.B1STU_highest_demand_15mins=user_B1STU_highest_demand_15mins
        self.plans=['B-10_SV', 'B-10_PV','B-10_TV','B-1','B-6','B-1-ST','A-1','B-10_S']
        

   def get_usage_hours(self,plan,peak_type,season):
          return self.Bundled_peak_time_df[
            (self.Bundled_peak_time_df['Sector'] == self.user_sector) &
            (self.Bundled_peak_time_df['Plan'] == plan) &
            (self.Bundled_peak_time_df['Type'] == peak_type) &
            (self.Bundled_peak_time_df['Season'] == season)]

   def set_summer_usage(self):
        self.summer_peak_usage = self.user_input_peak_usage
        self.summer_part_peak_usage = self.user_input_part_peak_usage
        self.summer_off_peak_usage = self.user_input_off_peak_usage
        return self.summer_peak_usage, self.summer_part_peak_usage, self.summer_off_peak_usage

   def set_winter_usage(self):
          self.winter_peak_usage = self.user_input_peak_usage
          self.winter_off_peak_usage = self.user_input_off_peak_usage
          self.winter_super_off_peak_usage = self.user_input_super_off_peak_usage
          self.winter_part_peak_usage = self.user_input_part_peak_usage
          return self.winter_peak_usage, self.winter_off_peak_usage,self.winter_super_off_peak_usage,self.winter_part_peak_usage

   def get_peak_times(self,df):
           start_time = df['Peak Start Time'].iloc[0] if not df['Peak Start Time'].empty else 'Other'
           stop_time= df['Peak End Time'].iloc[0] if not df['Peak End Time'].empty else 'Other'
           return start_time, stop_time

   def calculate(self):
     for plan in self.plans:
       if plan == 'B-10_S':
         usage=self.kwh_used
       else:
         if plan in ( 'B-10_SV', 'B-10_PV','B-10_TV','B-1'):
          for season in self.seasons:
           if season == 'Summer':
             summer_peak_usage,summer_part_peak_usage,summer_off_peak_usage=self.set_summer_usage()
             
             self.B10SVUSpeak_usage =summer_peak_usage
             self.B10SVUSpartpeak_usage = summer_part_peak_usage
             self.B10SVUSoffpeak_usage = summer_off_peak_usage

             self.B10PVUSpeak_usage = summer_peak_usage
             self.B10PVUSpartpeak_usage = summer_part_peak_usage
             self.B10PVUSoffpeak_usage = summer_off_peak_usage

             self.B10TVUSpeak_usage = summer_peak_usage
             self.B10TVUSpartpeak_usage = summer_part_peak_usage
             self.B10TVUSoffpeak_usage = summer_off_peak_usage

             self.B1USpeak_usage=summer_peak_usage
             self.B1USpartpeak_usage=summer_part_peak_usage
             self.B1USoffpeak_usage=summer_off_peak_usage

             peak_df = self.get_usage_hours(plan,'Peak','Summer')
             part_peak_df = self.get_usage_hours(plan,'Part-Peak','Summer')
             off_peak_df = self.get_usage_hours(plan,'Off-Peak','Summer')

             start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
             summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
             start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
             summer_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
             summer_off_peak_time_hours=24-summer_peak_time_hours-summer_part_peak_time_hours

             peak_range = list(range(16, 21))
             part_peak_range = list(range(14, 16)) + list(range(21, 23))
             peak_usage = ElectricUsage(summer_peak_usage, summer_peak_time_hours)
             part_peak_usage = ElectricUsage(summer_part_peak_usage, summer_part_peak_time_hours)
             off_peak_usage = ElectricUsage(summer_off_peak_usage, summer_off_peak_time_hours)
             usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)

             self.B10SVUWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
             self.B10SVUWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])
             self.B10SVUWsuperoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9, 14)])

             self.B10PVUWpeak_usage= self.B10SVUWpeak_usage
             self.B10PVUWoffpeak_usage= self.B10SVUWoffpeak_usage
             self.B10PVUWsuperoffpeak_usage= self.B10SVUWsuperoffpeak_usage

             self.B10TVUWpeak_usage= self.B10SVUWpeak_usage
             self.B10TVUWoffpeak_usage= self.B10SVUWoffpeak_usage
             self.B10TVUWsuperoffpeak_usage= self.B10SVUWsuperoffpeak_usage

             self.B1UWpeak_usage= self.B10SVUWpeak_usage
             self.B1UWoffpeak_usage= self.B10SVUWoffpeak_usage
             self.B1UWsuperoffpeak_usage= self.B10SVUWsuperoffpeak_usage

           elif season == 'Winter':
              winter_peak_usage,winter_off_peak_usage,winter_super_off_peak_usage,_=self.set_winter_usage()
              self.B10SVUWpeak_usage = winter_peak_usage
              self.B10SVUWoffpeak_usage = winter_off_peak_usage
              self.B10SVUWsuperoffpeak_usage = winter_super_off_peak_usage

              self.B10PVUWpeak_usage = winter_peak_usage
              self.B10PVUWoffpeak_usage = winter_off_peak_usage
              self.B10PVUWsuperoffpeak_usage = winter_super_off_peak_usage

              self.B10TVUWpeak_usage = winter_peak_usage
              self.B10TVUWoffpeak_usage = winter_off_peak_usage
              self.B10TVUWsuperoffpeak_usage = winter_super_off_peak_usage

              self.B1UWpeak_usage = winter_peak_usage
              self.B1UWoffpeak_usage = winter_off_peak_usage
              self.B1UWsuperoffpeak_usage = winter_super_off_peak_usage

              peak_df = self.get_usage_hours(plan,'Peak','Winter')
              super_off_df = self.get_usage_hours(plan,'Super-Off-Peak','Winter')

              start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
              winter_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
              start_time_super_off_peak, stop_time__super_off_peak = self.get_peak_times(super_off_df )
              winter_super_off_peak_time_hours=self.calculate_hours(start_time_super_off_peak,stop_time__super_off_peak)
              winter_off_peak_time_hours=24-winter_peak_time_hours-winter_super_off_peak_time_hours

              peak_range = list(range(16, 21))
              part_peak_range = list(range(9, 14)) 
              peak_usage = ElectricUsage(winter_peak_usage, winter_peak_time_hours)
              part_peak_usage = ElectricUsage(winter_super_off_peak_usage, winter_super_off_peak_time_hours)
              off_peak_usage = ElectricUsage(winter_off_peak_usage, winter_off_peak_time_hours)
              usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)

              self.B10SVUSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
              self.B10SVUSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 14)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(23, 24)])
              self.B19SVUSpartpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])

              self.B10PVUSpeak_usage= self.B10SVUSpeak_usage
              self.B10PVUSoffpeak_usage= self.B10SVUSoffpeak_usage
              self.B10PVUSpartpeak_usage= self.B19SVUSpartpeak_usage

              self.B10TVUStotalpeak_usage= self.B10SVUSpeak_usage
              self.B10TVUSoffpeak_usage= self.B10SVUSoffpeak_usage
              self.B10TVUSpartpeak_usage= self.B19SVUSpartpeak_usage

              self.B1USpeak_usage= self.B10SVUSpeak_usage
              self.B1USoffpeak_usage= self.B10SVUSoffpeak_usage
              self.B1USpartpeak_usage= self.B19SVUSpartpeak_usage

         if plan =='B-6':
          for season in self.seasons:
           if season == 'Summer':
             summer_peak_usage,_,summer_off_peak_usage=self.set_summer_usage()

             self.B6SUpeak_usage =summer_peak_usage
             self.B6SUoff_peak_usage = summer_off_peak_usage

             peak_df = self.get_usage_hours(plan,'Peak','Summer')

             start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
             summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
             summer_off_peak_time_hours=24-summer_peak_time_hours

             peak_range = list(range(16, 21))
             part_peak_range = []
             peak_usage = ElectricUsage(summer_peak_usage, summer_peak_time_hours)
             part_peak_usage = None
             off_peak_usage = ElectricUsage(summer_off_peak_usage, summer_off_peak_time_hours)
             usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)

             self.B6UWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
             self.B6UWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9,14)])
             self.B6UWsuperoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

           elif season == 'Winter':
               winter_peak_usage,winter_off_peak_usage,winter_super_off_peak_usage,_=self.set_winter_usage()

               self.B6UWpeak_usage =winter_peak_usage
               self.B6UWoffpeak_usage = winter_off_peak_usage
               self.B6UWsuperoffpeak_usage = winter_super_off_peak_usage

               peak_df = self.get_usage_hours(plan,'Peak','Winter')
               super_off_peak_df = self.get_usage_hours(plan,'Super-Off-Peak','Winter')

               start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
               winter_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
               start_time_super_off_peak, stop_time__super_off_peak = self.get_peak_times(super_off_peak_df)
               winter_super_off_peak_time_hours=self.calculate_hours(start_time_super_off_peak,stop_time__super_off_peak)
               winter_off_peak_time_hours=24-winter_peak_time_hours-winter_super_off_peak_time_hours

               peak_range = list(range(16, 21))
               part_peak_range = list(range(9, 14))
               peak_usage = ElectricUsage(winter_peak_usage, winter_peak_time_hours)
               part_peak_usage = ElectricUsage(winter_super_off_peak_usage, winter_super_off_peak_time_hours)
               off_peak_usage = ElectricUsage(winter_off_peak_usage, winter_off_peak_time_hours)
               usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)
           
               self.B6USpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
               self.B6USoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0,16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

         if plan=='B-1-ST':
          for season in self.seasons:
            if season == 'Summer':
                  summer_peak_usage,summer_part_peak_usage,summer_off_peak_usage=self.set_summer_usage()

                  self.B1STUSpeak_usage =summer_peak_usage
                  self.B1STUSpartpeak_usage = summer_part_peak_usage
                  self.B1STUSoffpeak_usage = summer_off_peak_usage

                  peak_df = self.get_usage_hours(plan,'Peak','Summer')
                  part_peak_df = self.get_usage_hours(plan,'Part-Peak','Summer')
                  off_peak_df = self.get_usage_hours(plan,'Off-Peak','Summer')

                  start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
                  summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
                  start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
                  summer_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
                  summer_off_peak_time_hours=24-summer_peak_time_hours-summer_part_peak_time_hours
                  
                  peak_range = list(range(16, 21))
                  part_peak_range = list(range(14, 16)) + list(range(21, 23))
                  peak_usage = ElectricUsage(summer_peak_usage, summer_peak_time_hours)
                  part_peak_usage = ElectricUsage(summer_part_peak_usage, summer_part_peak_time_hours)
                  off_peak_usage = ElectricUsage(summer_off_peak_usage, summer_off_peak_time_hours)
                  usage_dict = self.get_usage_dict(peak_range,part_peak_range, peak_usage, part_peak_usage, off_peak_usage)

                  self.B1STUWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
                  self.B1STUWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)])+ + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(23, 24)])
                  self.B1STUWsuperoff_peak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9, 14)])
                  self.B1STUWpartpeak_usage= sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])

            elif season  == 'Winter':
                 winter_peak_usage,winter_off_peak_usage,winter_super_off_peak_usage,winter_part_peak_usage=self.set_winter_usage()

                 self.B1STUWpeak_usage = winter_peak_usage
                 self.B1STUWoffpeak_usage = winter_off_peak_usage
                 self.B1STUWsuperoffpeak_usage = winter_super_off_peak_usage
                 self.B1STUWpartpeak_usage= winter_part_peak_usage

                 peak_df = self.get_usage_hours(plan,'Peak','Winter')
                 super_off_peak_df = self.get_usage_hours(plan,'Super-Off-Peak','Winter')
                 part_peak_df =  self.get_usage_hours(plan,'Part-Peak','Winter')

                 start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
                 winter_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
                 start_time_super_off_peak, stop_time__super_off_peak = self.get_peak_times(super_off_peak_df)
                 winter_super_off_peak_time_hours=self.calculate_hours(start_time_super_off_peak,stop_time__super_off_peak)
                 start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
                 winter_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
                 winter_off_peak_time_hours=24-winter_peak_time_hours-winter_super_off_peak_time_hours- winter_part_peak_time_hours
                 
                 usage_dict = {}
                 for hour in range(24):
                     if  hour in range(16, 21):
                         usage_dict[f'{hour}_oclock_usage'] = winter_peak_usage / winter_peak_time_hours
                     elif hour in range(9, 14):
                         usage_dict[f'{hour}_oclock_usage'] = winter_super_off_peak_usage / winter_super_off_peak_time_hours
                     elif hour in range(14, 16) or hour in range(21,23):
                         usage_dict[f'{hour}_oclock_usage'] = winter_part_peak_usage / winter_part_peak_time_hours
                     else:
                         usage_dict[f'{hour}_oclock_usage'] = winter_off_peak_usage / winter_off_peak_time_hours

                 self.B1STUSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
                 self.B1STUSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0,14)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(23, 24)])
                 self.B1STUSpartpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])

         if plan=='A-1':
          for season in self.seasons:
            if season == 'Summer':
              summer_peak_usage,summer_part_peak_usage,summer_off_peak_usage=self.set_summer_usage()

              self.A1NTUStotal_usage = summer_peak_usage+summer_part_peak_usage+summer_off_peak_usage
              self.A1USpeak_usage =summer_peak_usage
              self.A1USpartpeak_usage = summer_part_peak_usage
              self.A1USoffpeak_usage = summer_off_peak_usage

              peak_df = self.get_usage_hours(plan,'Peak','Summer')
              part_peak_df = self.get_usage_hours(plan,'Part-Peak','Summer')

              start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
              summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
              start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
              summer_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
              summer_off_peak_time_hours=24-summer_peak_time_hours-summer_part_peak_time_hours

              usage_dict = {}

              summer_peak_time_half_hours = summer_peak_time_hours * 2
              summer_part_peak_time_half_hours = summer_part_peak_time_hours * 2
              summer_off_peak_time_half_hours = summer_off_peak_time_hours * 2

              for half_hour in range(48):
                   hour = half_hour // 2
                   minute = (half_hour % 2) * 30
                   time_label = f'{hour:02d}:{minute:02d}'

                   if (12 <= hour < 18) or (hour == 18 and minute == 0):
                        usage_dict[f'{time_label}_usage'] = summer_peak_usage / summer_peak_time_half_hours
                   elif (8 <= hour < 12) or (hour == 12 and minute == 0) or (hour == 18 and minute == 30) or (18 < hour < 21) or (hour == 21 and minute == 30):  # 08:30 to 12:00 and 18:00 to 21:30
                        usage_dict[f'{time_label}_usage'] = summer_part_peak_usage / summer_part_peak_time_half_hours
                   else:  # All other times
                        usage_dict[f'{time_label}_usage'] = summer_off_peak_usage / summer_off_peak_time_half_hours

              self.A1UWpartpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(8, 22) for minute in [0, 30] if not (hour == 8 and minute == 0)])
              self.A1UWoffpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for half_hour in range(48) if (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(8, 22) for m in [0, 30]]])
            elif season== 'Winter':
                _,winter_off_peak_usage,_,winter_part_peak_usage=self.set_winter_usage()

                self.A1NTUWtotal_usage = winter_part_peak_usage+winter_off_peak_usage
                self.A1USpartpeak_usage = winter_part_peak_usage
                self.A1USoffpeak_usage = winter_off_peak_usage

                part_peak_df = self.get_usage_hours(plan,'Part-Peak','Winter')
                
                start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
                winter_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
                winter_off_peak_time_hours=24-winter_part_peak_time_hours

                usage_dict = {}
                winter_part_peak_time_half_hours = winter_part_peak_time_hours * 2
                winter_off_peak_time_half_hours = winter_off_peak_time_hours * 2

                for half_hour in range(48):
                    hour = half_hour // 2
                    minute = (half_hour % 2) * 30
                    time_label = f'{hour:02d}:{minute:02d}'

                    if (8 <= hour < 12) or (hour == 12 and minute == 0) or (hour == 18 and minute == 30) or (18 < hour < 21) or (hour == 21 and minute == 30):  # 08:30 to 12:00 and 18:00 to 21:30
                        usage_dict[f'{time_label}_usage'] = winter_part_peak_usage / winter_part_peak_time_half_hours
                    else:  # All other times
                        usage_dict[f'{time_label}_usage'] = winter_off_peak_usage / winter_off_peak_time_half_hours

                self.A1USpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(12, 18) for minute in [0, 30]])
                self.A1USpartpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(8, 12) for minute in [0, 30] if not (hour == 8 and minute == 0)]) + sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(18, 22) for minute in [0, 30]])
                self.A1USoffpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for half_hour in range(48) if (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(8, 12) for m in [0, 30]] and (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(18, 22) for m in [0, 30]] and (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(12, 18) for m in [0, 30]]])

   def update(self):
        self.calculate()
import pandas as pd
class SMBSector:
    def __init__(self, A1NTBStotal_usage, A1NTBWtotal_usage, A1BSpeak_usage,
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
        self.A1NTBStotal_usage = A1NTBStotal_usage
        self.A1NTBWtotal_usage = A1NTBWtotal_usage
        self.A1BSpeak_usage = A1BSpeak_usage
        self.A1BSpartpeak_usage = A1BSpartpeak_usage
        self.A1BSoffpeak_usage = A1BSoffpeak_usage
        self.A1BWpartpeak_usage = A1BWpartpeak_usage 
        self.A1BWoffpeak_usage = A1BWoffpeak_usage
        self.B1BSpeak_usage = B1BSpeak_usage
        self.B1BSpartpeak_usage = B1BSpartpeak_usage
        self.B1BSoffpeak_usage = B1BSoffpeak_usage
        self.B1BWpeak_usage = B1BWpeak_usage
        self.B1BWsuperoffpeak_usage = B1BWsuperoffpeak_usage
        self.B1BWoffpeak_usage = B1BWoffpeak_usage
        self.B1STBSpeak_usage = B1STBSpeak_usage
        self.B1STBSpartpeak_usage = B1STBSpartpeak_usage
        self.B1STBSoffpeak_usage = B1STBSoffpeak_usage
        self.B1STBWpeak_usage = B1STBWpeak_usage
        self.B1STBWpartpeak_usage = B1STBWpartpeak_usage
        self.B1STBWsuperoffpeak_usage = B1STBWsuperoffpeak_usage
        self.B1STBWoffpeak_usage = B1STBWoffpeak_usage
        self.B6BSpeak_usage = B6BSpeak_usage
        self.B6BSoffpeak_usage = B6BSoffpeak_usage
        self.B6BWpeak_usage = B6BWpeak_usage
        self.B6BWsuperoffpeak_usage = B6BWsuperoffpeak_usage
        self.B6BWoffpeak_usage = B6BWoffpeak_usage
        self.B10SVBSpeak_usage = B10SVBSpeak_usage
        self.B10SVBSpartpeak_usage = B10SVBSpartpeak_usage
        self.B10SVBSoffpeak_usage = B10SVBSoffpeak_usage
        self.B10SVBWpeak_usage = B10SVBWpeak_usage
        self.B10SVBWsuperoffpeak_usage = B10SVBWsuperoffpeak_usage
        self.B10SVBWoffpeak_usage = B10SVBWoffpeak_usage
        self.B10PVBSpeak_usage = B10PVBSpeak_usage
        self.B10PVBSpartpeak_usage = B10PVBSpartpeak_usage
        self.B10PVBSoffpeak_usage = B10PVBSoffpeak_usage
        self.B10PVBWpeak_usage = B10PVBWpeak_usage
        self.B10PVBWsuperoffpeak_usage = B10PVBWsuperoffpeak_usage
        self.B10PVBWoffpeak_usage = B10PVBWoffpeak_usage
        self.B10TVBSpeak_usage = B10TVBSpeak_usage
        self.B10TVBSpartpeak_usage = B10TVBSpartpeak_usage
        self.B10TVBSoffpeak_usage = B10TVBSoffpeak_usage
        self.B10TVBWpeak_usage = B10TVBWpeak_usage
        self.B10TVBWsuperoffpeak_usage = B10TVBWsuperoffpeak_usage
        self.B10TVBWoffpeak_usage = B10TVBWoffpeak_usage
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
        self.B1STB_highest_demand_15mins = B1STB_highest_demand_15mins

class SMBSector_simplified:
   def calculate_hours(self,start_time, stop_time):
          if start_time == 'Other' or stop_time == 'Other':
            return 0
          else:
            start_hour = start_time.hour
            stop_hour = stop_time.hour
            hours= stop_hour - start_hour
            return hours

   def __init__(self, user_input_peak_usage, user_input_part_peak_usage, user_input_super_off_peak_usage, user_input_off_peak_usage,meter_input,time_in_use,max_15min_usage, user_sector,user_B1STB_highest_demand_15mins,kwh_used):
        if(user_input_peak_usage<=23 or user_input_part_peak_usage<=23 or user_input_super_off_peak_usage<=23 or user_input_off_peak_usage<=23):
            raise ValueError('Minimum Peak usage not met,should be greater than 23')  
        self.Bundled_peak_time_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Bundled Peak Time Price')
        
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
        self.B1STB_highest_demand_15mins=user_B1STB_highest_demand_15mins
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
             
             self.B10SVBSpeak_usage =summer_peak_usage
             self.B10SVBSpartpeak_usage = summer_part_peak_usage
             self.B10SVBSoffpeak_usage = summer_off_peak_usage

             self.B10PVBSpeak_usage = summer_peak_usage
             self.B10PVBSpartpeak_usage = summer_part_peak_usage
             self.B10PVBSoffpeak_usage = summer_off_peak_usage

             self.B10TVBSpeak_usage = summer_peak_usage
             self.B10TVBSpartpeak_usage = summer_part_peak_usage
             self.B10TVBSoffpeak_usage = summer_off_peak_usage

             self.B1BSpeak_usage=summer_peak_usage
             self.B1BSpartpeak_usage=summer_part_peak_usage
             self.B1BSoffpeak_usage=summer_off_peak_usage

             peak_df = self.get_usage_hours(plan,'Peak','Summer')
             part_peak_df = self.get_usage_hours(plan,'Part-Peak','Summer')
             off_peak_df = self.get_usage_hours(plan,'Off-Peak','Summer')

             start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
             summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
             start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
             summer_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
             summer_off_peak_time_hours=24-summer_peak_time_hours-summer_part_peak_time_hours

             usage_dict = {}
             for hour in range(24):
                 if  hour in range(16, 21):
                      usage_dict[f'{hour}_oclock_usage'] = summer_peak_usage / summer_peak_time_hours
                 elif hour in range(14, 16) or hour in range(21,23):
                      usage_dict[f'{hour}_oclock_usage'] = summer_part_peak_usage / summer_part_peak_time_hours
                 else:
                      usage_dict[f'{hour}_oclock_usage'] = summer_off_peak_usage / summer_off_peak_time_hours

             self.B10SVBWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
             self.B10SVBWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])
             self.B10SVBWsuperoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9, 14)])

             self.B10PVBWpeak_usage= self.B10SVBWpeak_usage
             self.B10PVBWoffpeak_usage= self.B10SVBWoffpeak_usage
             self.B10PVBWsuperoffpeak_usage= self.B10SVBWsuperoffpeak_usage

             self.B10TVBWpeak_usage= self.B10SVBWpeak_usage
             self.B10TVBWoffpeak_usage= self.B10SVBWoffpeak_usage
             self.B10TVBWsuperoffpeak_usage= self.B10SVBWsuperoffpeak_usage

             self.B1BWpeak_usage= self.B10SVBWpeak_usage
             self.B1BWoffpeak_usage= self.B10SVBWoffpeak_usage
             self.B1BWsuperoffpeak_usage= self.B10SVBWsuperoffpeak_usage

           elif season == 'Winter':
              winter_peak_usage,winter_off_peak_usage,winter_super_off_peak_usage,_=self.set_winter_usage()
              self.B10SVBWpeak_usage = winter_peak_usage
              self.B10SVBWoffpeak_usage = winter_off_peak_usage
              self.B10SVBWsuperoffpeak_usage = winter_super_off_peak_usage

              self.B10PVBWpeak_usage = winter_peak_usage
              self.B10PVBWoffpeak_usage = winter_off_peak_usage
              self.B10PVBWsuperoffpeak_usage = winter_super_off_peak_usage

              self.B10TVBWpeak_usage = winter_peak_usage
              self.B10TVBWoffpeak_usage = winter_off_peak_usage
              self.B10TVBWsuperoffpeak_usage = winter_super_off_peak_usage

              self.B1BWpeak_usage = winter_peak_usage
              self.B1BWoffpeak_usage = winter_off_peak_usage
              self.B1BWsuperoffpeak_usage = winter_super_off_peak_usage

              peak_df = self.get_usage_hours(plan,'Peak','Winter')
              super_off_df = self.get_usage_hours(plan,'Super-Off-Peak','Winter')

              start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
              winter_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
              start_time_super_off_peak, stop_time__super_off_peak = self.get_peak_times(super_off_df )
              winter_super_off_peak_time_hours=self.calculate_hours(start_time_super_off_peak,stop_time__super_off_peak)
              winter_off_peak_time_hours=24-winter_peak_time_hours-winter_super_off_peak_time_hours
             
              usage_dict = {}
              for hour in range(24):
                 if  hour in range(16, 21):
                     usage_dict[f'{hour}_oclock_usage'] = winter_peak_usage / winter_peak_time_hours
                 elif hour in range(9, 14):
                     usage_dict[f'{hour}_oclock_usage'] = winter_super_off_peak_usage / winter_super_off_peak_time_hours
                 else:
                     usage_dict[f'{hour}_oclock_usage'] = winter_off_peak_usage / winter_off_peak_time_hours

              self.B10SVBSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
              self.B10SVBSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 14)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(23, 24)])
              self.B19SVBSpartpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])

              self.B10PVBSpeak_usage= self.B10SVBSpeak_usage
              self.B10PVBSoffpeak_usage= self.B10SVBSoffpeak_usage
              self.B10PVBSpartpeak_usage= self.B19SVBSpartpeak_usage

              self.B10TVBStotalpeak_usage= self.B10SVBSpeak_usage
              self.B10TVBSoffpeak_usage= self.B10SVBSoffpeak_usage
              self.B10TVBSpartpeak_usage= self.B19SVBSpartpeak_usage

              self.B1BSpeak_usage= self.B10SVBSpeak_usage
              self.B1BSoffpeak_usage= self.B10SVBSoffpeak_usage
              self.B1BSpartpeak_usage= self.B19SVBSpartpeak_usage

         if plan =='B-6':
          for season in self.seasons:
           if season == 'Summer':
             summer_peak_usage,_,summer_off_peak_usage=self.set_summer_usage()

             self.B6SBpeak_usage =summer_peak_usage
             self.B6SBoff_peak_usage = summer_off_peak_usage

             peak_df = self.get_usage_hours(plan,'Peak','Summer')

             start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
             summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
             summer_off_peak_time_hours=24-summer_peak_time_hours
<<<<<<< Updated upstream

=======
             
>>>>>>> Stashed changes
             usage_dict = {}
             for hour in range(24):
                 if  hour in range(16, 21):
                     usage_dict[f'{hour}_oclock_usage'] = summer_peak_usage / summer_peak_time_hours
                 else:
                     usage_dict[f'{hour}_oclock_usage'] = summer_off_peak_usage / summer_off_peak_time_hours

             self.B6BWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
             self.B6BWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9,14)])
             self.B6BWsuperoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)]) + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

           elif season == 'Winter':
               winter_peak_usage,winter_off_peak_usage,winter_super_off_peak_usage,_=self.set_winter_usage()

               self.B6BWpeak_usage =winter_peak_usage
               self.B6BWoffpeak_usage = winter_off_peak_usage
               self.B6BWsuperoffpeak_usage = winter_super_off_peak_usage

               peak_df = self.get_usage_hours(plan,'Peak','Winter')
               super_off_peak_df = self.get_usage_hours(plan,'Super-Off-Peak','Winter')

               start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
               winter_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
               start_time_super_off_peak, stop_time__super_off_peak = self.get_peak_times(super_off_peak_df)
               winter_super_off_peak_time_hours=self.calculate_hours(start_time_super_off_peak,stop_time__super_off_peak)
               winter_off_peak_time_hours=24-winter_peak_time_hours-winter_super_off_peak_time_hours

<<<<<<< Updated upstream
=======
               start_time_part_peak=super_off_peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
               stop_time_part_peak=super_off_peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
               winter_super_off_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)

               start_time_off_peak=off_peak_df['Peak Start Time'].iloc[0] if not peak_df['Peak Start Time'].empty else 'Other'
               stop_time_off_peak=off_peak_df['Peak End Time'].iloc[0] if not peak_df['Peak End Time'].empty else 'Other'
               winter_off_peak_time_hours=24-winter_peak_time_hours-winter_off_peak_time_hours

>>>>>>> Stashed changes
               usage_dict = {}
               for hour in range(24):
                 if  hour in range(16, 21):
                     usage_dict[f'{hour}_oclock_usage'] = winter_peak_usage / winter_peak_time_hours
                 elif hour in range(9, 14):
                     usage_dict[f'{hour}_oclock_usage'] = winter_super_off_peak_usage / winter_super_off_peak_time_hours
                 else:
                     usage_dict[f'{hour}_oclock_usage'] = winter_off_peak_usage / winter_off_peak_time_hours

               self.B6BSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
               self.B6BSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0,16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 24)])

<<<<<<< Updated upstream
         if plan=='B-1-ST':
=======
        if plan=='B-1-ST':
>>>>>>> Stashed changes
          for season in self.seasons:
            if season == 'Summer':
                  summer_peak_usage,summer_part_peak_usage,summer_off_peak_usage=self.set_summer_usage()

                  self.B1STBSpeak_usage =summer_peak_usage
                  self.B1STBSpartpeak_usage = summer_part_peak_usage
                  self.B1STBSoffpeak_usage = summer_off_peak_usage

                  peak_df = self.get_usage_hours(plan,'Peak','Summer')
                  part_peak_df = self.get_usage_hours(plan,'Part-Peak','Summer')
                  off_peak_df = self.get_usage_hours(plan,'Off-Peak','Summer')

                  start_time_peak, stop_time_peak = self.get_peak_times(peak_df)
                  summer_peak_time_hours=self.calculate_hours(start_time_peak,stop_time_peak)
                  start_time_part_peak, stop_time_part_peak = self.get_peak_times(part_peak_df)
                  summer_part_peak_time_hours=self.calculate_hours(start_time_part_peak,stop_time_part_peak)
                  summer_off_peak_time_hours=24-summer_peak_time_hours-summer_part_peak_time_hours
<<<<<<< Updated upstream

=======
                  
>>>>>>> Stashed changes
                  usage_dict = {}
                  for hour in range(24):
                     if  hour in range(16, 21):
                         usage_dict[f'{hour}_oclock_usage'] = summer_peak_usage / summer_peak_time_hours
                     elif hour in range(14, 16) or hour in range(21,23):
                         usage_dict[f'{hour}_oclock_usage'] = summer_part_peak_usage / summer_part_peak_time_hours
                     else:
                         usage_dict[f'{hour}_oclock_usage'] = summer_off_peak_usage / summer_off_peak_time_hours

                  self.B1STBWpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
                  self.B1STBWoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0, 9)])+ + sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(23, 24)])
                  self.B1STBWsuperoff_peak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(9, 14)])
                  self.B1STBWpartpeak_usage= sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])

            elif season  == 'Winter':
                 winter_peak_usage,winter_off_peak_usage,winter_super_off_peak_usage,winter_part_peak_usage=self.set_winter_usage()

                 self.B1STBWpeak_usage = winter_peak_usage
                 self.B1STBWoffpeak_usage = winter_off_peak_usage
                 self.B1STBWsuperoffpeak_usage = winter_super_off_peak_usage
                 self.B1STBWpartpeak_usage= winter_part_peak_usage

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

                 self.B1STBSpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(16, 21)])
                 self.B1STBSoffpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(0,14)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(23, 24)])
                 self.B1STBSpartpeak_usage = sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(14, 16)])+ sum([usage_dict[f'{hour}_oclock_usage'] for hour in range(21, 23)])

         if plan=='A-1':
          for season in self.seasons:
            if season == 'Summer':
              summer_peak_usage,summer_part_peak_usage,summer_off_peak_usage=self.set_summer_usage()

              self.A1NTBStotal_usage = summer_peak_usage+summer_part_peak_usage+summer_off_peak_usage
              self.A1BSpeak_usage =summer_peak_usage
              self.A1BSpartpeak_usage = summer_part_peak_usage
              self.A1BSoffpeak_usage = summer_off_peak_usage

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

              self.A1BWpartpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(8, 22) for minute in [0, 30] if not (hour == 8 and minute == 0)])
              self.A1BWoffpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for half_hour in range(48) if (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(8, 22) for m in [0, 30]]])
            elif season== 'Winter':
                _,winter_off_peak_usage,_,winter_part_peak_usage=self.set_winter_usage()

                self.A1NTBWtotal_usage = winter_part_peak_usage+winter_off_peak_usage
                self.A1BSpartpeak_usage = winter_part_peak_usage
                self.A1BSoffpeak_usage = winter_off_peak_usage

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

                self.A1BSpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(12, 18) for minute in [0, 30]])
                self.A1BSpartpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(8, 12) for minute in [0, 30] if not (hour == 8 and minute == 0)]) + sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for hour in range(18, 22) for minute in [0, 30]])
                self.A1BSoffpeak_usage = sum([usage_dict[f'{hour:02d}:{minute:02d}_usage'] for half_hour in range(48) if (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(8, 12) for m in [0, 30]] and (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(18, 22) for m in [0, 30]] and (half_hour // 2, (half_hour % 2) * 30) not in [(h, m) for h in range(12, 18) for m in [0, 30]]])

   def update(self):
        self.calculate()
        
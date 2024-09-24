# -*- coding: utf-8 -*-
"""Hass6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Zer9W6IKRHaXBo3lcasszuCt-BOGoWd0
"""

from attendee import AttendeeDistribution
from haasevent import HaasEvent


class CalculateEmission:
  
  def set_nonstudent_distrib(self):
    train_percent_non_student = 0.02
    bike_percent_non_student = 0.3
    car_percent_non_student = 0.61 # added 0.01 since total was 0.99
    flight_percent_non_student = 0.05
    bus_percent_non_student = 0.02 
    self.nonstudent_distribution = AttendeeDistribution(train_percent_non_student, bike_percent_non_student, car_percent_non_student, flight_percent_non_student, bus_percent_non_student )

  def set_student_distrib(self):
    train_percent_student = 0.04
    bike_percent_student = 0.6 # added 0.1 since total was 0.9
    car_percent_student = 0.3
    flight_percent_student = 0.01
    bus_percent_student = 0.05
    self.student_distribution = AttendeeDistribution(train_percent_student,bike_percent_student, car_percent_student, flight_percent_student, bus_percent_student )

  def __init__(self):    
    self.set_student_distrib()
    self.set_nonstudent_distrib()
    
  def get_emission_range(self, distrib, event, distrib_percentage):
     min = distrib_percentage * event.ci_distribution[0]
     mean = distrib_percentage * event.mean_attendance
     max = distrib_percentage * event.ci_distribution[1]

     emissions_min = distrib.calculate_emissions(min)
     emissions_mean = distrib.calculate_emissions(mean)
     emissions_max = distrib.calculate_emissions(max)
     return (emissions_min, emissions_mean, emissions_max)
     
  def get_haas_event_tuples(self):
   emission_obj = []
   for event in self.haas_events:
      student_emissions = self.student_distribution.get_emission_dict(event.mean_attendance, event.student_percentage)  
      nonstudent_emissions = self.nonstudent_distribution.get_emission_dict(event.mean_attendance, event.non_student_percentage)   
      emission_obj.append({
         "student": student_emissions,
         "nonstudent": nonstudent_emissions
         })
   return emission_obj
  
  def calculate_haas_events_emissions(self):
   emission_obj = []
   for event in self.haas_events:
      emissions_student_obj = self.get_emission_range(self.student_distribution, event, event.student_percentage)
      emissions_nonstudent_obj = self.get_emission_range(self.nonstudent_distribution, event, event.non_student_percentage)

      event.save_emissions(emissions_student_obj, emissions_nonstudent_obj)
      student_intensity = emissions_student_obj[1] / event.student_attendance
      non_student_intensity = emissions_nonstudent_obj[1] / event.non_student_attendance

      emission_obj.append( {
         "student": event.emissions_student_obj,
         "nonstudent": event.emissions_nonstudent_obj,
         "mean_attendance": event.mean_attendance,
         "mean_student_intensity": student_intensity,
         "non_student_intensity": non_student_intensity,
         })
   return emission_obj
  
  def set_haas_events(self, haas_events):
     self.haas_events = haas_events

def create_haas_events(num_attendees, event_type, event_location, event_time):
    haas_events = []
    range = 0
    if num_attendees < 75 and num_attendees > 25:
       range = 7
    elif num_attendees < 150:
       range = 15
    else:
       range = 25
    
    min = num_attendees - range
    max = num_attendees + range
    estimated_attendance = [min, max]

    # TODO expect to match the eventtype with the student/non-student distribution
    if event_type == "lunch":
        student = .85
        non_student = .15
    elif event_type == "conference":
        student = .85
        non_student = .15
    elif event_type == "industry_sector":
        student = .50
        non_student = .50
    elif event_type == "celebration":
        student = .70
        non_student = .30
    elif event_type == "career_fair":
        student = .80
        non_student = .20

    haas_event = HaasEvent(estimated_attendance, student, non_student, event_location, event_time)
    haas_events.append(haas_event)
    return haas_events

import pandas as pd
from openpyxl import Workbook

def read_excel_sheet():
    df = pd.read_excel('haas/input_csv/haas_report_1727043593.xlsx', sheet_name='event_totals')
    return df

def process_event_data(row):
    print(row)
    return create_haas_events(row['attendees'], row['event_type'], row['location'], row['event_date'])

def write_new_excelsheet(tuples):
    wb = Workbook()
    ws_emissions = wb.active
    ws_emissions.title = "transportation"

    # Define headers
    headers = [
        "student-train", "student-car", "student-plane", "student-bus", "student-bike",
        "nonstudent-train", "nonstudent-car", "nonstudent-plane", "nonstudent-bus", "nonstudent-bike"
    ]
    ws_emissions.append(headers)

    # Write data
    for tup in tuples:
        row_data = []
        for category in ['student', 'nonstudent']:
            for transport in ['train', 'car', 'plane', 'bus', 'bike']:
                row_data.append(tup[category][transport])
        ws_emissions.append(row_data)

    try:
        wb.save('haas/output_csv/haas_emissions_report.xlsx')
        print("Excel file saved successfully.")
    except Exception as e:
        print(f"Error saving Excel file: {e}")
        print("Attempting to handle the error...")
        
        if isinstance(e, FileNotFoundError):
            print("The output directory doesn't exist. Please check the path.")
        elif isinstance(e, PermissionError):
            print("Permission denied. Please check file permissions.")
        else:
            print("Unexpected error occurred. Please check your data and try again.")
        
        # You might want to implement a fallback save method here
        # For example, saving to a different location or format

def main():
    calculate_emissions = CalculateEmission()
    
    # Read the Excel sheet
    df = read_excel_sheet()
    
    # Process each row and create HaasEvent objects
    all_haas_events = []
    for _, row in df.iterrows():
        haas_events = process_event_data(row)
        all_haas_events.extend(haas_events)
    
    # Set HaasEvents and calculate emissions
    calculate_emissions.set_haas_events(all_haas_events)
    emissions = calculate_emissions.calculate_haas_events_emissions()
    tuples = calculate_emissions.get_haas_event_tuples()

    print("Emissions are:")
    print(emissions)

    print("Tuples are:")
    print(tuples)

    # Write results to a new Excel sheet
    write_new_excelsheet(tuples)

    print("Results have been written to 'haas/output/haas_emissions_report.xlsx'")
    
    '''
    TODO food waste
    read every row of food sheet from haas/input_csv/haas_report_1727043593.xlsx
    then, for each row, use the function food_waste_calculator() to calculate the
    emissions abmount based on the food category it falls into from 
    haas/food_waste_category.py
    then, use the function food_waste_disposal_probability() to calculate the 
    probability of each food waste disposal method for each food category
    '''

def food_waste_calculator(food_category):
   #@pbryzk get the carbonssutain.io food waste calculation logic and put it here
   return
if __name__ == '__main__':
    main()

#For Students
#Number people bike,train,plane ...
#Total emissions for each
# Total final emissions

#For Non-Students
#Number people bike,train,plane ...
#Total emissions for each
# Total final emissions
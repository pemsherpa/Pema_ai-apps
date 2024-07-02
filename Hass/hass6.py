# -*- coding: utf-8 -*-
"""Hass6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Zer9W6IKRHaXBo3lcasszuCt-BOGoWd0
"""

from attendee import AttendeeDistribution


class CalculateEmission:
  def set_avg_distances(self):
    # Distances in avg miles traveled
    self.train_distance = 20
    self.car_distance = 10
    self.bike_distance = 5
    self.plane_distance = 350
    self.bus_distance = 15
  
  def set_emission_factors(self):
    # Emission factors
    self.train_emission = 0.056
    self.car_emission = 0.347
    self.plane_emission = 0.396
    self.bus_emission = 0.177
    self.bike_emission = 0

  def create_distribution_obj(self, train_percent_student, bike_percent_student, car_percent_student, plane_percent_student, bus_percent_student, attendee_percent):
    ci_distribution = [self.min_attendance*attendee_percent, self.max_attendance*attendee_percent]
    return AttendeeDistribution(train_percent_student,bike_percent_student, car_percent_student, plane_percent_student, bus_percent_student, ci_distribution )
      
  def __init__(self,estimated_attance,student,non_student):
    self.min_attendance = estimated_attance[0]
    self.max_attendance = estimated_attance[1]
    self.mean_attance = (self.min_attendance + self.max_attendance) // 2
    self.student_percent = student
    self.non_student_percent = non_student
    
    train_percent_student = 0.05
    bike_percent_student = 0.6
    car_percent_student = 0.4
    plane_percent_student = 0.01
    bus_percent_student = 0.04
    self.student_distribution = self.create_distribution_obj(train_percent_student, bike_percent_student, car_percent_student, plane_percent_student, bus_percent_student, self.student_percent)
    
    train_percent_non_student = 0.03
    bike_percent_non_student = 0.3
    car_percent_non_student = 0.6
    plane_percent_non_student = 0.05
    bus_percent_non_student = 0.02    
    self.non_student_distribution = self.create_distribution_obj(train_percent_non_student, bike_percent_non_student, car_percent_non_student, plane_percent_non_student, bus_percent_non_student, self.non_student_percent)

    self.set_avg_distances()
    self.set_emission_factors()

  def calculate_emission_element(self, min, distrib_obj):
     emission_element = self.train_distance*self.train_emission*min+self.car_distance*self.car_emission*min + self.bike_distance*self.bike_emission*min+self.plane_distance*self.plane_emission*min + self.bus_distance*self.bus_emission*min
     return emission_element
  
  def calculate_emission_group(self, min, max, distrib_obj):
     emission_group = [self.calculate_emission_element(min, distrib_obj),
                       self.calculate_emission_element(max, distrib_obj)]
     return emission_group

  def calculate_emission(self):
    student_emission = self.calculate_emission_group(self.student_distribution.ci_attendance[0], self.student_distribution.ci_attendance[1], self.student_distribution)
    non_student_emission = self.calculate_emission_group(self.non_student_distribution.ci_attendance[0], self.non_student_distribution.ci_attendance[1], self.non_student_distribution)

    return (student_emission,non_student_emission)


def main():
    estimated_attance = [101, 125]
    student = .85
    non_student = .15

    calculate_emissions = CalculateEmission(estimated_attance, student, non_student)
    emissons = calculate_emissions.calculate_emission()
    print(emissons)

if __name__ == '__main__':
    main()
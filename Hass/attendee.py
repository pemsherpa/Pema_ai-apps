class AttendeeDistribution:
  def __init__(self, train_percent,bike_percent,car_percent, plane_percent, bus_percent):
    self.train_percent = train_percent
    self.bike_percent = bike_percent
    self.car_percent = car_percent
    self.plane_percent = plane_percent
    self.bus_percent = bus_percent

    self.check_total()
    self.set_avg_distances()
    self.set_emission_factors()

  def set_avg_distances(self):
    # Distances in avg miles traveled
    self.train_distance = 20
    self.car_distance = 10
    self.plane_distance = 350
    self.bus_distance = 15
    self.bike_distance = 5
  
  def set_emission_factors(self):
    # Emission factors
    self.train_emission = 0.056
    self.car_emission = 0.347
    self.plane_emission = 0.396
    self.bus_emission = 0.177
    self.bike_emission = 0

  def check_total(self):
    total_percent = self.train_percent + self.bike_percent + self.car_percent + self.plane_percent + self.bus_percent
    if total_percent > 1.0:
       print("check_total: total_percent greater than 1.0 " + str(total_percent))
       return
    elif total_percent < 1.0:
       msg = "check_total: total_percent less than 1.0 " + str(total_percent)
       print(msg)
       raise Exception(msg)
  
  def calculate_train_emissions(self, num_attendees):
    emissions = self.train_distance * self.train_emission * (num_attendees * self.train_percent)
    return emissions
  
  def calculate_car_emissions(self, num_attendees):
    emissions = self.car_distance * self.car_emission * (num_attendees * self.car_percent)
    return emissions
  
  def calculate_plane_emissions(self, num_attendees):
    emissions = self.plane_distance * self.plane_emission * (num_attendees * self.plane_percent)
    return emissions
  
  def calculate_bus_emissions(self, num_attendees):
    emissions = self.bus_distance * self.bus_emission * (num_attendees * self.bus_percent)
    return emissions
  
  def calculate_bike_emissions(self, num_attendees):
    emissions = self.bike_distance * self.bike_emission * (num_attendees * self.bike_percent)
    round_emissions = round(emissions, 3)
    return round_emissions
  
  def get_emission_dict(self, num_attendees):
    train_emissions = self.calculate_train_emissions(num_attendees)
    car_emissions = self.calculate_car_emissions(num_attendees)
    plane_emissions = self.calculate_plane_emissions(num_attendees)
    bus_emissions = self.calculate_bus_emissions(num_attendees)
    bike_emissions = self.calculate_bike_emissions(num_attendees)

    return {"train": train_emissions, "car": car_emissions, "plane": plane_emissions, "bus": bus_emissions, "bike": bike_emissions}
  
  def calculate_emissions(self, num_attendees):
    train_emissions = self.calculate_train_emissions(num_attendees)
    car_emissions = self.calculate_car_emissions(num_attendees)
    plane_emissions = self.calculate_plane_emissions(num_attendees)
    bus_emissions = self.calculate_bus_emissions(num_attendees)
    bike_emissions = self.calculate_bike_emissions(num_attendees)

    total_emissions = train_emissions + car_emissions + plane_emissions + bus_emissions + bike_emissions

    return total_emissions




    

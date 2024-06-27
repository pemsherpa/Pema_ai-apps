from geopy.distance import geodesic
import requests
import time
from itertools import permutations

class BusinessCommutingAnalyzer:
    def __init__(self, commuting_data,google_api,oil_price_api,firm_location,df_dynamic):
        self.commuting_data = commuting_data
        self.google_maps_api_key = google_api
        self.oil_api = oil_price_api
        self.firm_location = firm_location
        self.df_dynamic = df_dynamic

        cur_people = self.commuting_data
        cur_people_location = cur_people['locations']

        employee_coords = [self.geocode_location(location) for location in cur_people_location]
        firm_coords = self.geocode_location(firm_location)

        if None in employee_coords or firm_coords is None:
            print("Failed to geocode all locations.")
            return None

        # Calculate distances
        distances_from_firm = [geodesic(firm_coords, coord).kilometers for coord in employee_coords]
        cur_people['distance'] = distances_from_firm
        self.commuting_data = cur_people
        print(self.commuting_data)

    def calculate_current_costs_and_emissions(self):
        total_cost = 0
        total_carbon = 0
        print(self.commuting_data)
        for index, row in self.commuting_data.iterrows():
            distance = row['distance']
            frequency = row['frequency']
            cost_per_km = row['cost_per_km']
            total_cost += distance * frequency * cost_per_km
            total_carbon += distance * frequency * cost_per_km * 0.2

        return total_cost, total_carbon

    def geocode_location(self,location):
      # (latitude, longitude) using Google Maps Geocoding API
      base_url = "https://maps.googleapis.com/maps/api/geocode/json"
      params = {
          "address": location,
          "key": self.google_maps_api_key
      }
      response = requests.get(base_url, params=params)
      if response.status_code == 200:
          data = response.json()
          if data['results']:
              latitude = data['results'][0]['geometry']['location']['lat']
              longitude = data['results'][0]['geometry']['location']['lng']
              return (latitude, longitude)
      return None

    def get_state_code(self,coords):
      base_url = "https://maps.googleapis.com/maps/api/geocode/json"
      params = {"latlng": f"{coords[0]},{coords[1]}", "key": self.google_maps_api_key}
      response = requests.get(base_url, params=params)
      data = response.json()
      if response.status_code == 200 and data['results']:
          for component in data['results'][0]['address_components']:
              if 'administrative_area_level_1' in component['types']:
                  return component['short_name']
      return None

    def calculate_distance(self,location1, location2):
      """Calculate the distance between two geographical coordinates."""
      coords_1 = self.geocode_location(location1)
      time.sleep(10)
      coords_2 = self.geocode_location(location2)

      if coords_1 and coords_2:
          return geodesic(coords_1, coords_2).kilometers
      else:
          return None

    def get_local_gas_price(self,state_code):
      if self.oil_api:
          base_url = f"https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key={self.oil_api}&frequency=weekly&data[0]=value&facets[duoarea][]=S{state_code}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=1"
          response = requests.get(base_url)
          data = response.json()
          print(f"API response: {data}")
          if response.status_code == 200 and 'response' in data and 'data' in data['response'] and len(data['response']['data']) > 0:
              return float(data['response']['data'][0]['value'])
      print(f"Failed to retrieve gas price for state: {state_code}")
      return 4

    def stipent_individual(self,df_survey,firm_location,employee_ID, cur_stipend, num_change_days,mpg):
      cur_person = df_survey.loc[df_survey['ID'] == employee_ID,['locations','frequency']]
      state_code = self.get_state_code(self.geocode_location(cur_person['locations']))
      cur_person['cost_per_km'] = (self.get_local_gas_price(state_code)/mpg) / 1.609344
      firm_coords = self.geocode_location(firm_location)
      employee_coords = self.geocode_location(cur_person['locations'])
      distance = geodesic(firm_coords, employee_coords).kilometers
      cur_person['distance'] = distance
      cur_cost = cur_person['distance'].values[0] * cur_person['frequency'].values[0] * cur_person['cost_per_km'].values[0]

      dic = {}
      dic_cash = {}
      optimal = cur_cost

      for method in self.df_dynamic['method'].unique():
          temp = self.df_dynamic.loc[self.df_dynamic['method'] == method]
          if not temp.empty:
              temp_cost_new = temp['distance'].values[0] * num_change_days * temp['cost_per_km'].values[0]
              cost_original = (cur_person['frequency'].values[0] - num_change_days) * cur_person['distance'].values[0] * cur_person['cost_per_km'].values[0]
              new_cost = temp_cost_new + cost_original

              if new_cost < cur_stipend:
                  cash = (cur_stipend - new_cost) * 0.9  # This factor can be adjusted
                  dic_cash[method] = cash

              dic[method] = new_cost

              if new_cost < optimal:
                  optimal = new_cost

      return dic, dic_cash, optimal

    def get_directions(self,origin, destination, waypoints=[]):
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": "|".join(waypoints),
            "key": self.google_maps_api_key,
            "departure_time": "now"
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200 and data['routes']:
            return data['routes'][0]
        else:
            print(f"Error: {data.get('error_message')} | Status: {data.get('status')}")
        return None

    def find_optimal_route(self,firm_location, employee_locations):
        best_route = None
        best_order = None
        min_distance = float('inf')
        min_duration = float('inf')

        # Generate all possible orders for the waypoints
        for order in permutations(employee_locations):
            for i in range(len(order)):
                waypoints = list(order[:i]) + list(order[i+1:])  # All waypoints except the final destination
                final_destination = order[i]  # The i-th location in the order is the final destination
                route = self.get_directions(firm_location, final_destination, waypoints=waypoints)

                if route:
                    total_distance = sum(leg['distance']['value'] for leg in route['legs']) / 1000  # Convert to kilometers
                    total_duration = sum(leg['duration']['value'] for leg in route['legs']) / 60  # Convert to minutes
                    if total_distance < min_distance:
                        min_distance = total_distance
                        min_duration = total_duration
                        best_route = route
                        best_order = waypoints + [final_destination]  # Append final destination at the end

        if best_route:
            return {
                "route": best_route,
                "total_distance_km": min_distance,
                "total_duration_min": min_duration,
                "optimal_order": best_order
            }
        return None

    def carpool_savings(self, df_survey, firm_location, employee_ids, cur_stipend, num_carpool_days, mpg):

      # Get the current details of each person
      firm_coords = self.geocode_location(firm_location)
      cur_people = df_survey[df_survey['ID'].isin(employee_ids)]
      cur_people_location = cur_people['locations']
      employee_coords = [self.geocode_location(location) for location in cur_people_location]
      if None in employee_coords or firm_coords is None:
          print("Failed to geocode all locations.")
          return None

        # Calculate distances
      distances_from_firm = [geodesic(firm_coords, coord).kilometers for coord in employee_coords]

      cur_people['distance'] = distances_from_firm
      # caveat
      state_code = self.get_state_code(self.geocode_location(cur_people['locations']))

      cur_people['cost_per_km'] = (self.get_local_gas_price(state_code)/mpg) / 1.609344
      cur_costs = cur_people.apply(lambda row: row['distance'] * row['frequency'] * row['cost_per_km'], axis=1)

      optimal_distance = self.find_optimal_route(firm_location, cur_people_location)['total_distance_km']
      duration = self.find_optimal_route(firm_location, cur_people_location)['total_duration_min']
      carpool_cost = min(cur_people['cost_per_km'] )
      new_cost_carpool_days = (optimal_distance*num_carpool_days*carpool_cost)

      new_cost_original_days = cur_people['distance']*cur_people['cost_per_km']*(cur_people['frequency']-num_carpool_days)
      new_cost_total = new_cost_carpool_days+new_cost_original_days
      new_carbon = duration*0.2

      net_cost = new_cost_total - cur_costs
      cash = net_cost*0.9
      return net_cost,cash,new_carbon
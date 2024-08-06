import math
import requests
import pandas as pd

class Flight:
    def __init__(self, non_stop, flight_class, airplane_model, departure_airport, arrival_airport,cost, stops=[]):
        self.non_stop = non_stop
        self.flight_class = flight_class
        self.airplane_model = airplane_model
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.stops = stops
        self.cost=cost

class FlightEmissionsCalculator:
    KG_CONVERSION = 0.453592

    def __init__(self, emissions_file, api_key):
        self.emissions_df = pd.read_excel(emissions_file)
        self.emissions_dict = self.emissions_df.set_index('Airplane Model')['Emissions (kg/passenger/mile)'].to_dict()
        self.api_key = api_key

    def get_coordinates(self, iata_code):
        url = f"https://api.geoapify.com/v1/geocode/search?text={iata_code} airport&apiKey={self.api_key}"

        headers = {
            "Accept": "application/json"
        }

        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            if "features" in data and len(data["features"]) > 0:
                lat = data['features'][0]['properties']['lat']
                lon = data['features'][0]['properties']['lon']
                return lat, lon
            else:
                return None, None
        else:
            print(f"Error: {resp.status_code}")
            return None, None

    def get_distance_haversine_formula(self, lat1, lon1, lat2, lon2):
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        R_km = 6371.0

        distance_km = R_km * c

        distance_miles = distance_km * 0.621371
        return distance_miles

    def calculate_total_distance(self, flight):
        if flight.non_stop:
            return self.calculate_flight_distance(flight)
        else:
            total_distance = 0
            stops = flight.stops
            for leg in stops:
                lat1, lon1 = self.get_coordinates(leg.departure_airport)
                lat2, lon2 = self.get_coordinates(leg.arrival_airport)
                if lat1 and lon1 and lat2 and lon2:
                    leg_distance = self.get_distance_haversine_formula(lat1, lon1, lat2, lon2)
                    total_distance += leg_distance
                else:
                    return 0
            return total_distance

    def calculate_flight_distance(self, flight):
        lat1, lon1 = self.get_coordinates(flight.departure_airport)
        lat2, lon2 = self.get_coordinates(flight.arrival_airport)
        if lat1 and lon1 and lat2 and lon2:
            distance = self.get_distance_haversine_formula(lat1, lon1, lat2, lon2)
            return distance
        else:
            return 0

    def calculate_flight_emissions(self, flight, distance):
         if flight.non_stop:
            airplane_model = flight.airplane_model
            flight_class = flight.flight_class
         else:
            airplane_model = flight.stops[0].airplane_model
            flight_class = flight.stops[0].flight_class

         model_emission_rate = self.emissions_dict.get(airplane_model, 0)

         class_emission_rates = {
            "Economy": 0.44 * self.KG_CONVERSION,
            "Premium Economy": 0.55 * self.KG_CONVERSION,
            "Business": 1.29 * self.KG_CONVERSION,
            "First": 2.1 * self.KG_CONVERSION 
        }
         class_emission_rate = class_emission_rates.get(flight_class, 0)

         total_emission_rate = model_emission_rate + class_emission_rate

         stops = flight.stops
         if stops:
            num_stops = len(stops)
            total_emission_rate *= (1 + 0.10 * num_stops)

         total_emissions = total_emission_rate * distance
         return total_emissions

    def calculate_total_distance_and_emissions(self, flight):
        total_distance = self.calculate_total_distance(flight)
        total_emissions = self.calculate_flight_emissions(flight, total_distance)
        return total_distance, total_emissions

    def find_optimized_flight(self, flight):
        original_distance, original_emissions = self.calculate_total_distance_and_emissions(flight)

        alternative_flights = []
        has_stops = not flight.non_stop

        for model in self.emissions_dict.keys():
            for flight_class in ["Economy", "Premium Economy", "Business", "First"]:
                alternative_flight = Flight(
                    non_stop=True if has_stops else flight.non_stop,
                    flight_class=flight_class,
                    airplane_model=model,
                    departure_airport=flight.departure_airport,
                    arrival_airport=flight.arrival_airport,
                    cost=flight.cost
                )

                if has_stops:
                    alternative_flight.stops = []

                distance, emissions = self.calculate_total_distance_and_emissions(alternative_flight)
                if emissions is not None:
                    alternative_flights.append({
                        "airplane_model": model,
                        "class": flight_class,
                        "distance": distance,
                        "emissions": emissions
                    })

        optimized_flight = min(alternative_flights, key=lambda x: x["emissions"])

        return original_distance, original_emissions, optimized_flight

    def carbon_saved(self, original_emissions, optimized_emissions):
        return original_emissions - optimized_emissions

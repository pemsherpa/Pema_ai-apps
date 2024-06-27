import requests
import pandas as pd
from datetime import datetime

class FlightDataAnalyzer:
    def __init__(self, api_key, weights,origin, destination, departure_date, return_date=None):
        self.api = api_key
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.weights = weights

        self.flights_economy = self.search_flights_serpapi(origin, destination, departure_date, '1', return_date)
        self.flights_premium_economy = self.search_flights_serpapi(origin, destination, departure_date, '2', return_date)
        self.flights_business = self.search_flights_serpapi(origin, destination, departure_date, '3', return_date)
        self.flights_first_class = self.search_flights_serpapi(origin, destination, departure_date, '4', return_date)

        self.df_economy = self.create_dataframes_serpapi(self.flights_economy)
        self.df_premium_economy = self.create_dataframes_serpapi(self.flights_premium_economy)
        self.df_business = self.create_dataframes_serpapi(self.flights_business)
        self.df_first_class = self.create_dataframes_serpapi(self.flights_first_class)

        self.df_all_flights = pd.concat([self.df_economy, self.df_business, self.df_first_class, self.df_premium_economy], ignore_index=True)

        self.df_all_flights['Departure Time'] = pd.to_datetime(self.df_all_flights['Departure Time'])
        self.df_all_flights['Arrival Time'] = pd.to_datetime(self.df_all_flights['Arrival Time'])

    def get_optimal_flight(self, df_all_flights):
        df_all_flights['Price Z-Score'] = (df_all_flights['Price'] - df_all_flights['Price'].mean()) / df_all_flights['Price'].std()
        df_all_flights['Duration Z-Score'] = (df_all_flights['Duration'] - df_all_flights['Duration'].mean()) / df_all_flights['Duration'].std()
        df_all_flights['Stops Z-Score'] = (df_all_flights['Stops'] - df_all_flights['Stops'].mean()) / df_all_flights['Stops'].std()
        df_all_flights['Carbon Emissions Z-Score'] = (df_all_flights['Carbon Emissions'] - df_all_flights['Carbon Emissions'].mean() )/ df_all_flights['Carbon Emissions'].std()

        df_all_flights['Weighted Score'] = (
            self.weights.price_weight * df_all_flights['Price Z-Score'] +
            self.weights.duration_weight * df_all_flights['Duration Z-Score'] +
            self.weights.stop_weight * df_all_flights['Stops Z-Score'] +
            self.weights.carbon_weight * df_all_flights['Carbon Emissions Z-Score']
        )

        df_all_flights['Rank'] = df_all_flights['Weighted Score'].rank()
        df_best_trade_off_flights = df_all_flights.sort_values(by='Rank').head(1)
        return df_best_trade_off_flights

    def get_return_tickets(self):
        temp  = self.get_optimal_flight(self.df_all_flights)
        self.dep_token = temp['token'].iloc[0]

        return_flights_economy = self.search_flights_serpapi(self.origin, self.destination, self.departure_date, '1', self.return_date, token=self.dep_token)
        return_flights_premium_economy = self.search_flights_serpapi(self.origin, self.destination, self.departure_date, '2', self.return_date, token=self.dep_token)
        return_flights_business = self.search_flights_serpapi(self.origin, self.destination, self.departure_date, '3', self.return_date, token=self.dep_token)
        return_flights_first_class = self.search_flights_serpapi(self.origin, self.destination, self.departure_date, '4', self.return_date, token=self.dep_token)

        df_return_flights_economy = self.create_dataframes_serpapi(return_flights_economy)
        df_return_flights_premium_economy = self.create_dataframes_serpapi(return_flights_premium_economy)
        df_return_flights_business = self.create_dataframes_serpapi(return_flights_business)
        df_return_flights_first_class = self.create_dataframes_serpapi(return_flights_first_class)

        all_return_flights = pd.concat([df_return_flights_economy, df_return_flights_business, df_return_flights_first_class, df_return_flights_premium_economy], ignore_index=True)
        return self.get_optimal_flight(all_return_flights)

    def create_dataframes_serpapi(self, flights):
        columns = ['Carrier', 'Flight Number', 'Departure Airport', 'Departure Time', 'Arrival Airport', 'Arrival Time', 'Duration',
                   'Aircraft', 'Carbon Emissions', 'Typical Carbon Emissions', 'Difference in Percent', 'Travel Class',
                   'Price', 'Stops', 'Layovers', 'Total Duration','token']
        flight_data = []
        seen_flights = set()

        def extract_flight_data(flight_list):
            for flight in flight_list:
                price = flight['price']
                stops = len(flight['flights']) - 1
                layovers = flight.get('layovers', 'N/A')
                total_duration = flight['total_duration']
                if 'departure_token' in flight:
                    token = flight['departure_token']
                else:
                    token = 'N/A'

                for i, segment in enumerate(flight['flights']):
                    carrier_code = segment['airline']
                    flight_number = segment['flight_number']
                    departure = segment['departure_airport']['id']
                    departure_time = segment['departure_airport']['time']
                    arrival = segment['arrival_airport']['id']
                    arrival_time = segment['arrival_airport']['time']
                    duration = segment['duration']
                    aircraft = segment['airplane']

                    carbon_emissions = flight['carbon_emissions']['this_flight']
                    if flight['carbon_emissions']['typical_for_this_route']:
                        typical_carbon_emissions = flight['carbon_emissions']['typical_for_this_route']
                        difference_in_percent = flight['carbon_emissions']['difference_percent']
                    else:
                         typical_carbon_emissions = 'N/A'
                         difference_in_percent = 'N/A'

                    travel_class_name = segment['travel_class']

                    flight_key = (carrier_code, flight_number, departure_time, arrival_time)
                    if flight_key not in seen_flights:
                        seen_flights.add(flight_key)
                        flight_data.append([
                            carrier_code, flight_number, departure, departure_time,
                            arrival, arrival_time, duration, aircraft, carbon_emissions, typical_carbon_emissions, difference_in_percent, travel_class_name,
                            price, stops, layovers, total_duration,token
                        ])

        if 'best_flights' in flights:
            extract_flight_data(flights['best_flights'])

        if 'other_flights' in flights:
            extract_flight_data(flights['other_flights'])

        df_flights = pd.DataFrame(flight_data, columns=columns)
        return df_flights
    
    def price_insights(self):
        lst_economy = self.flights_economy['price_insights']['price_history']

        lst_business = self.flights_business['price_insights']['price_history']

        temp_df_economy = pd.DataFrame(lst_economy, columns=['time', 'price'])
        temp_df_economy['time'] = temp_df_economy['time'].apply(datetime.fromtimestamp)

        temp_df_business = pd.DataFrame(lst_business, columns=['time', 'price'])
        temp_df_business['time'] = temp_df_business['time'].apply(datetime.fromtimestamp)

        graph_economy = temp_df_economy.plot.line(x='time', y='price')
        graph_business = temp_df_business.plot.line(x='time', y='price')

        info_economy = self.flights_economy['price_insights']['price_history'][:-1]
        info_business = self.flights_business['price_insights']['price_history'][:-1]
 
        return info_economy, info_business, graph_economy,  graph_business

    def search_flights_serpapi(self, origin, destination, departure_date, travel_class, return_date=None, token=None):
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_flights",
            "q": f"flights from {origin} to {destination} on {departure_date}",
            "api_key": self.api,
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date,
            "type": "1" if return_date else "2",  # 1 for round trip; 2 for one way
            "show_hidden": "true",
            "travel_class": travel_class
        }
        if return_date:
            params["return_date"] = return_date
        if token:
            params["departure_token"] = token

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def compare_stops(self):
        # Calculate median price by number of stops and travel class
        out = self.df_all_flights.groupby(['Stops', 'Travel Class'])['Price'].median().unstack()
        return out

    def non_economy_cheaper_than_economy(self):
        median_price_economy = self.df_all_flights[self.df_all_flights['Travel Class'] == 'Economy']['Price'].median()
        non_economy_cheaper_than_economy = self.df_all_flights[(self.df_all_flights['Travel Class'] != 'Economy') & (self.df_all_flights['Price'] <= median_price_economy)]
        return non_economy_cheaper_than_economy

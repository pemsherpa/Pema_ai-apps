
class ElectricityBillAnalyzer:
    def __init__(self, providers):
        self.providers = providers

    def analyze_bill(self, bill):
        location = bill['location']
        total_consumption_kwh = bill['total_consumption_kwh']
        current_cost_per_kwh = bill['total_cost'] / total_consumption_kwh

        # Filter providers by location
        local_providers = [p for p in self.providers if p['location'] == location]

        # Compare providers
        comparisons = []
        for provider in local_providers:
            new_cost = provider['cost_per_kwh'] * total_consumption_kwh
            cost_savings = (current_cost_per_kwh - provider['cost_per_kwh']) * total_consumption_kwh
            new_carbon = provider['carbon_per_kwh'] * total_consumption_kwh
            carbon_savings = (current_cost_per_kwh - provider['carbon_per_kwh']) * total_consumption_kwh
            comparisons.append({
                'provider': provider['name'],
                'new_cost': new_cost,
                'cost_savings': cost_savings,
                'new_carbon': new_carbon,
                'carbon_savings': carbon_savings
            })

        return comparisons
    #def region_finder(self):


    def recommend_providers(self, bill):
        recommendations = self.analyze_bill(bill)
        recommendations.sort(key=lambda x: (x['new_cost'], x['new_carbon']))

        return recommendations

    def analyze_historical_data(self, historical_data):
        # Analyze historical data to identify consumption patterns
        total_consumption = sum(record['consumption_kwh'] for record in historical_data)
        total_cost = sum(record['cost'] for record in historical_data)
        average_consumption = total_consumption / len(historical_data)
        average_cost = total_cost / len(historical_data)

        return {
            'total_consumption_kwh': total_consumption,
            'total_cost': total_cost,
            'average_consumption_kwh': average_consumption,
            'average_cost': average_cost
        }

    def compare_tariffs(self, current_tariff, new_tariffs):
        # Compare different tariff plans
        comparisons = []
        for tariff in new_tariffs:
            if 'peak_rate' in tariff and 'off_peak_rate' in tariff:
                peak_consumption = current_tariff['peak_consumption_kwh']
                off_peak_consumption = current_tariff['off_peak_consumption_kwh']
                new_cost = (tariff['peak_rate'] * peak_consumption) + (tariff['off_peak_rate'] * off_peak_consumption)
            else:
                new_cost = tariff['flat_rate'] * current_tariff['total_consumption_kwh']
            cost_savings = current_tariff['total_cost'] - new_cost
            comparisons.append({
                'tariff_name': tariff['name'],
                'new_cost': new_cost,
                'cost_savings': cost_savings
            })

        return comparisons

    def suggest_carbon_offsets(self, carbon_savings):
        # Suggest carbon offset programs
        offset_programs = [
            {'name': 'Program A', 'cost_per_kg_co2': 0.01},
            {'name': 'Program B', 'cost_per_kg_co2': 0.02}
        ]
        # offset gives you amt carbon saving * price of object, in this case, electricity
        suggestions = []
        for program in offset_programs:
            offset_cost = program['cost_per_kg_co2'] * carbon_savings
            suggestions.append({
                'program_name': program['name'],
                'offset_cost': offset_cost
            })

        return suggestions

    def analyze_solar_panel(self, bill, solar_capacity_kw, solar_cost_per_kw, maintenance_cost_per_year, solar_carbon_per_kwh,day, hour):
        location = bill['location']
        total_consumption_kwh = bill['total_consumption_kwh']
        current_cost_per_kwh = bill['total_cost'] / total_consumption_kwh

        annual_solar_production_kwh = solar_capacity_kw * day * hour  #hours of peak sunlight per day
        initial_solar_cost = solar_capacity_kw * solar_cost_per_kw
        annual_solar_maintenance_cost = maintenance_cost_per_year
        total_annual_savings = current_cost_per_kwh * annual_solar_production_kwh
        net_annual_savings = total_annual_savings - annual_solar_maintenance_cost
        total_savings = net_annual_savings - initial_solar_cost
        new_carbon = solar_carbon_per_kwh * annual_solar_production_kwh
        carbon_savings = current_cost_per_kwh * total_consumption_kwh - new_carbon

        return {
            'solar_capacity_kw': solar_capacity_kw,
            'initial_solar_cost': initial_solar_cost,
            'annual_solar_maintenance_cost': annual_solar_maintenance_cost,
            'annual_solar_production_kwh': annual_solar_production_kwh,
            'total_annual_savings': total_annual_savings,
            'net_annual_savings': net_annual_savings,
            'total_savings': total_savings,
            'new_carbon': new_carbon,
            'carbon_savings': carbon_savings
        }


    def notify_user(self, email, message):

        print(f"Sending email to {email} with message: {message}")

    def integrate_with_ui(self, user_input):
        # Placeholder for UI integration
        bill = user_input['bill']
        recommendations = self.recommend_providers(bill)
        return recommendations


import pandas as pd
from datetime import datetime
from steps.quarterly_step import QuarterStep
from steps.decarb_step_type import DecarbStepType
from steps.provider_info import ProviderInfo

# Load the dataset
dataset_electric = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Joint Rate Plan')

class Electric_Recommendations:
    def __init__(self, current_provider, electric_step, cur_year, cur_quarter):
        self.electric_step = electric_step
        self.electric_plan = electric_step.get_new_plan(HasCCA='Yes')
        self.optimized_plan = self.electric_plan
        self.current_provider = current_provider

        '''if cur_year is None or cur_quarter is None:
            current_date = datetime.now()
            self.cur_year = current_date.year
            self.cur_quarter = (current_date.month - 1) // 3 + 1  # Calculate quarter from current month
        else:
            self.cur_year = cur_year
            self.cur_quarter = cur_quarter'''

        # Initialize the current renewable percentage
        if current_provider in dataset_electric["Electrical Company Name"].values:
            self.current_renew_percent = dataset_electric.loc[
                dataset_electric["Electrical Company Name"] == self.current_provider,
                "Renewable Percentages"
            ].values[0]
        else:
            raise ValueError("Current provider not found.")

        self.cur_year = cur_year
        self.cur_quarter = cur_quarter
        self.quarter_steps = []
        self.recommendations = []
        self.recommended_providers = set()  # To avoid redundancy
        self.jrp_plans_df = dataset_electric  # Reference to the data for provider info
        self.generate_recommendations(5)  # Plans for 5 years

    def generate_recommendations(self, years):
        for year in range(0, years):
            recommendation = self.recommend_plan(self.cur_year+year)
            
            print(recommendation)
            self.recommendations.append(recommendation)

            # Update state based on the recommendation
            if recommendation['recommended_plan'] == 50:
                self.current_renew_percent = 50
                self.update_provider(recommendation['New Provider'])
            elif recommendation['recommended_plan'] == 100:
                self.current_renew_percent = 100
                self.update_provider(recommendation['New Provider'])

            self.cur_year += (self.cur_quarter // 4)
            self.cur_quarter = (self.cur_quarter % 4) + 1

    def update_provider(self, new_providers):
        for provider in new_providers:
            if provider not in self.recommended_providers:
                self.current_provider = provider
                self.recommended_providers.add(provider)
                break

    def recommend_plan(self, year):
        if self.current_renew_percent == 100:
            return {
                "year": year,
                "recommended_plan": 100,
                "message": "Continue using 100% renewable energy.",
                "New Provider": [],
                "carbon_emission_savings": 0,
                "provider_info": []
            }

        # Calculate carbon emission savings
        carbon_emission_savings = self.electric_step.compute_emissions_savings()

        if year == 1:
            new_plan_name = self.optimized_plan
            new_company = self.get_company_for_plan(new_plan_name)
            provider_infos = self.get_provider_info(new_plan_name)
            return {
                "year": year,
                "recommended_plan": new_plan_name,
                "message": f"Switch to the {new_plan_name} plan.",
                "Providers of this plan": list(set(dataset_electric.loc[
                    dataset_electric["Plan"] == new_plan_name, "Electrical Company Name"].tolist())),
                "carbon_emission_savings": carbon_emission_savings,
                "provider_info": [str(info) for info in provider_infos]
            }

        if year == 2 or self.current_renew_percent < 50:
            new_providers = self.get_unique_providers(50, self.current_renew_percent)
            provider_infos = [info for provider in new_providers for info in self.get_provider_info(self.optimized_plan, provider)]
            return {
                "year": year,
                "recommended_plan": 50,
                "message": "Switch to a plan with at least 50% renewable energy.",
                "New Provider": new_providers,
                "provider_info": provider_infos
            }

        if year >= 3 and self.current_renew_percent < 100:
            new_providers = self.get_unique_providers(100, self.current_renew_percent)
            provider_infos = [info for provider in new_providers for info in self.get_provider_info(self.optimized_plan, provider)]
            return {
                "year": year,
                "recommended_plan": 100,
                "message": "Switch to a plan with 100% renewable energy.",
                "New Provider": new_providers,
                "provider_info": provider_infos
            }

        return {
            "year": year,
            "recommended_plan": self.current_renew_percent,
            "message": "Continue with the current plan.",
            "New Provider": [],
            "carbon_emission_savings": 0,
            "provider_info": []
        }

    def get_unique_providers(self, target_percent, current_percent):
        """
        Retrieves unique providers offering plans that meet the target renewable percentage and exceed the current percentage.
        """
        providers = dataset_electric.loc[
            (dataset_electric["Renewable Percentages"] >= target_percent) &
            (dataset_electric["Renewable Percentages"] > current_percent) &
            (~dataset_electric["Electrical Company Name"].isin(self.recommended_providers)),
            "Electrical Company Name"
        ].tolist()
        return list(set(providers))

    def get_company_for_plan(self, plan_name):
        """
        Retrieves a company associated with a specific plan name.
        """
        companies = dataset_electric.loc[dataset_electric["Plan"] == plan_name, "Electrical Company Name"].tolist()
        return companies[0] if companies else None

    def get_provider_info(self, plan_name, company=None):
        """
        Retrieves the provider information such as phone number and URL for all companies associated with the given plan name.
        """
        if company:
            df = self.jrp_plans_df[
                (self.jrp_plans_df['Plan'] == plan_name) & 
                (self.jrp_plans_df['Electrical Company Name'] == company)
            ]
        else:
            df = self.jrp_plans_df[self.jrp_plans_df['Plan'] == plan_name]
        
        provider_infos = []
        for _, row in df.iterrows():
            provider_number = row['Phone Number of provider']
            company_link = row['URL of the provider']
            provider_info = ProviderInfo(plan_name, row['Electrical Company Name'], provider_number, company_link)
            provider_infos.append(provider_info)
        
        return provider_infos
    
    def to_dict(self):
        # Converts recommendations to a dictionary format
        return {
            "current_provider": self.current_provider,
            "current_renew_percent": self.current_renew_percent,
            "cur_year": self.cur_year,
            "cur_quarter": self.cur_quarter,
            "recommendations": [rec for rec in self.recommendations],
            "recommended_providers": list(self.recommended_providers),
        }









import pandas as pd
from steps.cru_recommendation import CRU_Recommendation
from steps.provider_info_cru import ProviderInfoCru

# Load the dataset containing CRU provider information
cru_providers_df = pd.read_excel('CRU_Providers.xlsx', sheet_name="Sheet1")

# Remove any leading or trailing whitespace in column names
cru_providers_df.columns = cru_providers_df.columns.str.strip()

class CRU_Recommendations:
    def __init__(self, provider_info, cru_step, cur_year, current_quarter,new_cost):
        self.cru_step = cru_step
        self.provider_info = provider_info
        self.cur_year = cur_year
        self.current_quarter = current_quarter
        self.recommendations = []
        self.provider_index = 0  # Track which companies were printed last
        self.total_providers = len(cru_providers_df)  # Total number of companies
        self.new_cost=new_cost

        # Generate CRU recommendations for the next 5 years
        self.generate_recommendations(5)


    def generate_recommendations(self, year):
        recommendation = self.recommend_plan(year)
        self.recommendations.append(recommendation)

    def recommend_plan(self, year):
        # Calculate carbon emission and cost savings
        carbon_emission_savings = self.cru_step.compute_emissions_savings()
        cost_savings = self.cru_step.compute_savings()

        # Filter provider infos and get message based on the estimation
        provider_infos, first_provider_info, message = self.get_provider_info()

        # Return the CRU recommendation
        return CRU_Recommendation(
            year,
            f"Switch to the optimized plan for carbon removal.",
            message,
            carbon_emission_savings,
            cost_savings,
            provider_infos,
            first_provider_info
        )

    def get_provider_info(self):
        """
        Retrieves the provider information for CRU providers and iterates over two companies each year.
        Ensures proper wrapping around when all companies have been iterated over.
        """
        provider_infos = []
        first_provider_info = None
        message = ""

        max_companies_per_year = 2

        # Calculate the start and end index for the current year
        start_idx = self.provider_index
        end_idx = start_idx + max_companies_per_year

        # Debugging: Print index information
        print(f"Start index: {start_idx}, End index: {end_idx}")

        # Handle wrapping around if we exceed the total number of companies
        if end_idx > self.total_providers:
            # Get the companies from start_idx to end, and then wrap around from 0 to the remainder
            current_providers_df = pd.concat([cru_providers_df.iloc[start_idx:], cru_providers_df.iloc[:end_idx % self.total_providers]])
        else:
            # Normal case, no wrapping needed
            current_providers_df = cru_providers_df.iloc[start_idx:end_idx]

        # Debugging: Print the selected companies for this iteration
        print("Selected companies for this year:")
        print(current_providers_df)

        # Iterate through the selected companies
        for _, row in current_providers_df.iterrows():
            estimation_value = row['Estimation']
            company = row['Provider']
            phone_number = row['Mobile']
            website_link = row['Website Link']
            description = row['Description']
            provider_type = row['Type']
            location = row['Location']

            # Retrieve carbon and cost savings
            carbon_emission_savings = self.cru_step.compute_emissions_savings()
            cost_savings = self.cru_step.compute_savings()

            # Create provider info object
            provider_info = ProviderInfoCru(
                company, phone_number, website_link, description,
                provider_type, carbon_emission_savings, cost_savings, location,self.new_cost
            )
            provider_infos.append(provider_info)

            # Keep track of the first provider info
            if first_provider_info is None:
                first_provider_info = provider_info

            # Generate the message based on the estimation value
            message="Welcome to Carbon Savings"
        # Update provider index for the next year
        self.provider_index = (self.provider_index + max_companies_per_year) % self.total_providers

        # Debugging: Print the updated provider index
        print(f"Updated provider index for next year: {self.provider_index}")

        return provider_infos, first_provider_info, message

    def to_dict(self):
        # Converts recommendations to a dictionary format
        return [rec.to_json() for rec in self.recommendations]
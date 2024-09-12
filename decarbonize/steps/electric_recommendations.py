import pandas as pd
from steps.electric_recommendation import Electric_Recommendation
from steps.provider_info import ProviderInfo

# Load the main dataset and the unbundled and bundled sheets
dataset_electric = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Joint Rate Plan')
unbundled_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Unbundled Peak Time Price')
bundled_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Bundled Peak Time Price')

class Electric_Recommendations:
    def __init__(self, current_provider, electric_step, cur_year, cur_quarter):
        self.electric_step = electric_step
        self.electric_plan = electric_step.get_new_plan(HasCCA='Yes')
        self.optimized_plan = self.electric_plan
        self.current_provider = current_provider

        # Initialize the current renewable percentage
        if current_provider in dataset_electric["Electrical Company Name"].values:
            self.current_renew_percent = dataset_electric.loc[
                dataset_electric["Electrical Company Name"] == self.current_provider,
                "Renewable Percentages"].values[0]
        else:
            raise ValueError("Current provider not found in the dataset.")

        print("Initial Current Renewable Percentage:", self.current_renew_percent)

        self.cur_year = cur_year
        self.cur_quarter = cur_quarter
        self.quarter_steps = []
        self.recommendations = []
        self.recommended_providers = set()  # To avoid redundancy
        self.jrp_plans_df = dataset_electric  # Reference to the data for provider info
        self.generate_recommendations(5)  # Plans for 5 years

    def generate_recommendations(self, years):
        for year in range(0, years):
            recommendation = self.recommend_plan(self.cur_year + year)
            print(f"Year: {self.cur_year + year}, Recommended Plan: {recommendation.recommended_plan}")

            self.recommendations.append(recommendation)

            # Update state based on the recommendation
            if recommendation.recommended_plan in [50, 100]:
                self.current_renew_percent = recommendation.recommended_plan

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
            return Electric_Recommendation(year, 100, "Continue using 100% renewable energy.", 0, 0,0,0, [], [])

        # Calculate carbon emission savings
        carbon_emission_savings = self.electric_step.compute_emissions_savings()
        cost_savings = self.electric_step.compute_savings()

        if year == self.cur_year:
            new_plan_name = self.optimized_plan
            provider_infos, first_provider_info = self.get_provider_info(new_plan_name)
            optimized_plan_renew_percent = self.get_renewable_percent(new_plan_name)

            # Get peak and off-peak prices for the optimized plan
            peak_price, off_peak_price = self.get_peak_off_peak_prices(new_plan_name)

            return Electric_Recommendation(
                year,
                self.optimized_plan,
                f"Switch to the {new_plan_name} plan.",
                carbon_emission_savings,
                cost_savings,
                peak_price,
                off_peak_price,
                provider_infos,
                first_provider_info
            )

        # Year 2: Recommend 50% renewable plan if necessary
        if year == self.cur_year + 1 and self.current_renew_percent < 50:
            new_providers = self.get_unique_providers(50, self.current_renew_percent)
            provider_infos = []
            first_provider_info = None
            for provider in new_providers:
                infos, first_info = self.get_provider_info(self.optimized_plan, provider)
                provider_infos.extend(infos)
                if first_provider_info is None:
                    first_provider_info = first_info
            
            peak_price, off_peak_price = self.get_peak_off_peak_prices(self.optimized_plan)

            return Electric_Recommendation(
                year,
                50,
                "Switch to a plan with at least 50% renewable energy.",
                carbon_emission_savings,
                cost_savings,
                peak_price,
                off_peak_price,
                provider_infos,
                first_provider_info
            )

        # From year 3 onwards: Recommend 100% renewable plans
        if year >= self.cur_year + 2:
            new_providers = self.get_unique_providers(100, self.current_renew_percent)
            provider_infos = []
            first_provider_info = None
            for provider in new_providers:
                infos, first_info = self.get_provider_info(self.optimized_plan, provider)
                provider_infos.extend(infos)
                if first_provider_info is None:
                    first_provider_info = first_info
            
            peak_price, off_peak_price = self.get_peak_off_peak_prices(self.optimized_plan)

            return Electric_Recommendation(
                year,
                100,
                "Switch to a plan with 100% renewable energy.",
                carbon_emission_savings,
                cost_savings,
                peak_price,
                off_peak_price,
                provider_infos,
                first_provider_info
            )

        return Electric_Recommendation(year, self.current_renew_percent, "Continue with the current plan.", 0, 0,0,0, [], None)

    def get_peak_off_peak_prices(self, plan_name):
        
     # Filter rows for the given plan name
        unbundled_price = unbundled_df.loc[unbundled_df['Plan'] == plan_name]
        bundled_price = bundled_df.loc[bundled_df['Plan'] == plan_name]

    # Initialize peak and off-peak prices
        peak_price = None
        off_peak_price = None

        if not unbundled_price.empty:
        # Find peak and off-peak prices in the unbundled dataframe
            peak_row = unbundled_price[unbundled_price['Type'].str.lower() == 'peak']
            off_peak_row = unbundled_price[unbundled_price['Type'].str.lower() == 'off-peak']
            peak_price = peak_row['Customer Charge Rate'].iloc[0] if not peak_row.empty else None
            off_peak_price = off_peak_row['Customer Charge Rate'].iloc[0] if not off_peak_row.empty else None

        if not bundled_price.empty:
        # Find peak and off-peak prices in the bundled dataframe if not found in unbundled
            if peak_price is None:
                peak_row = bundled_price[bundled_price['Type'].str.lower() == 'peak']
                peak_price = peak_row['Customer Charge Rate'].iloc[0] if not peak_row.empty else None
            if off_peak_price is None:
                off_peak_row = bundled_price[bundled_price['Type'].str.lower() == 'off-peak']
                off_peak_price = off_peak_row['Customer Charge Rate'].iloc[0] if not off_peak_row.empty else None

        return peak_price, off_peak_price


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
        first_provider_info = None
        for _, row in df.iterrows():
            provider_number = row['Phone Number of provider']
            company_link = row['URL of the provider']
            provider_info = ProviderInfo(plan_name, row['Electrical Company Name'], provider_number, company_link)
            provider_infos.append(provider_info)

            if first_provider_info is None:
                first_provider_info = provider_info
        
        return provider_infos, first_provider_info

    def get_renewable_percent(self, plan_name):
        """
        Retrieves the renewable percentage of a specific plan.
        """
        row = dataset_electric.loc[dataset_electric["Plan"] == plan_name]
        if not row.empty:
            return row["Renewable Percentages"].values[0]
        return 0

    def to_dict(self):
        # Converts recommendations to a dictionary format
        return {
            "current_provider": self.current_provider,
            "recommendations": [rec.to_json() for rec in self.recommendations]
        }

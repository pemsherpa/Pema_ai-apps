import pandas as pd
from steps.electric_recommendation import Electric_Recommendation
from steps.provider_info import ProviderInfo

# Load the main dataset and the unbundled and bundled sheets
dataset_electric = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Joint Rate Plan')
unbundled_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Unbundled Peak Time Price')
bundled_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Bundled Peak Time Price')

class Electric_Recommendations:
    def __init__(self, current_provider, electric_step, cur_year, cur_quarter,new_cost):
        self.electric_step = electric_step
        self.electric_plan = electric_step.get_new_plan(HasCCA='Yes')
        self.optimized_plan = self.electric_plan
        self.current_provider = current_provider
        self.new_cost=new_cost

        # Initialize the current renewable percentage
        if current_provider in dataset_electric["Electrical Company Name"].values:
            self.current_renew_percent = dataset_electric.loc[
                dataset_electric["Electrical Company Name"] == self.current_provider,
                "Renewable Percentages"].values[0]
        else:
            raise ValueError("Current provider not found in the dataset.")

        self.cur_year = cur_year
        self.cur_quarter = cur_quarter
        self.quarter_steps = []
        self.recommendations = []
        self.recommended_providers = set()  # To avoid redundancy
        self.jrp_plans_df = dataset_electric  # Reference to the data for provider info
        self.generate_recommendations(5)  # Plans for 5 years

    def generate_recommendations(self, years):
        temp_year = self.cur_year
        temp_quarter = self.cur_quarter
        for year in range(0, years):
            print(self.cur_year + year)
            recommendation = self.recommend_plan(self.cur_year + year)
            print(f"Year: {self.cur_year + year}, Recommended Plan: {recommendation.recommended_plan}")

            if recommendation.recommended_plan == 100:
                self.current_renew_percent = 100

            self.recommendations.append(recommendation)

            # Update state based on the recommendation
            if recommendation.recommended_plan in [50, 100]:
                self.current_renew_percent = recommendation.recommended_plan

            temp_quarter += 1
            if temp_quarter > 4:
               temp_quarter = 1
               temp_year += 1

    
            self.cur_year = temp_year
            self.cur_quarter = temp_quarter

    def recommend_plan(self, year):
        # Calculate carbon emission and cost savings

        provider_infos = []
        first_provider_info = None

        # Year 1: Recommend plans with renewable percentages less than 50%
        if year == self.cur_year:
            new_providers = self.get_unique_providers(49.5, self.current_renew_percent)
            for provider in new_providers:
                infos, first_info = self.get_provider_info(self.optimized_plan, provider)
                provider_infos.extend(infos)
                if first_provider_info is None:
                    first_provider_info = first_info

            return Electric_Recommendation(
                self.optimized_plan,
                "Switch to a plan with atmost 50% renewable energy.",
                provider_infos,
                first_provider_info
            )

        # Year 2: Recommend plans with renewable percentages between 50% and 75%
        elif year == self.cur_year + 1:
            new_providers = self.get_unique_providers(75, self.current_renew_percent)
            new_providers = [p for p in new_providers if 50 <= self.get_renewable_percent(p) < 75]
            for provider in new_providers:
                infos, first_info = self.get_provider_info(self.optimized_plan, provider)
                provider_infos.extend(infos)
                if first_provider_info is None:
                    first_provider_info = first_info

            return Electric_Recommendation(
                "50-75% Renewable Plan",
                "Switch to a plan with renewable energy between 50% and 75%.",
                provider_infos,
                first_provider_info
            )

        # Year 3: Recommend only 100% renewable plans
        elif year == self.cur_year + 2:
            new_providers = self.get_unique_providers(100, self.current_renew_percent)
            new_providers = [p for p in new_providers if self.get_renewable_percent(p) == 100]
            for provider in new_providers:
                infos, first_info = self.get_provider_info(self.optimized_plan, provider)
                provider_infos.extend(infos)
                if first_provider_info is None:
                    first_provider_info = first_info

            return Electric_Recommendation(
                "100% Renewable Plan",
                "Switch to a plan with 100% renewable energy.",
                provider_infos,
                first_provider_info
            )

        # Year 4 and beyond: Recommend continuing with 100% renewable energy
        elif year >= self.cur_year + 3:
            new_providers = self.get_unique_providers(100, self.current_renew_percent)
            new_providers = [p for p in new_providers if self.get_renewable_percent(p) == 100]
            for provider in new_providers:
                infos, first_info = self.get_provider_info(self.optimized_plan, provider)
                provider_infos.extend(infos)
                if first_provider_info is None:
                    first_provider_info = first_info

            return Electric_Recommendation(
                100,
                "Continue using 100% renewable energy.",
                provider_infos,
                first_provider_info
                
            )

        # Default recommendation
        return Electric_Recommendation(
            100,
            "Continue with the current plan.",
            [], None
        )

    def get_unique_providers(self, target_percent, current_percent):
        """
        Retrieves a unique list of providers based on renewable percentages and whether they have been recommended.
        """
        providers = dataset_electric.loc[
            (dataset_electric["Renewable Percentages"] <= target_percent) &
            (dataset_electric["Renewable Percentages"] >= current_percent) &
            (~dataset_electric["Electrical Company Name"].isin(self.recommended_providers))
        ].groupby("Electrical Company Name").first().index.tolist()

        # Include the current provider if it meets the condition and hasn't been recommended yet
        if self.current_provider not in self.recommended_providers and \
            self.get_renewable_percent(self.current_provider) >= current_percent:
            providers.append(self.current_provider)

        return list(set(providers))

    def get_provider_info(self, plan_name, company=None):
    
        if company:
            df = self.jrp_plans_df[
            (self.jrp_plans_df['Plan'] == plan_name) & 
            (self.jrp_plans_df['Electrical Company Name'] == company)
        ]
        else:
            df = self.jrp_plans_df[self.jrp_plans_df['Plan'] == plan_name]
        
        
        provider_infos = {}
        first_provider_info = None

        carbon_emission_savings = self.electric_step.compute_emissions_savings()
        cost_savings = self.electric_step.compute_savings()
        carbon_emission_savings = format(carbon_emission_savings, ".2f")
        cost_savings = format(cost_savings, ".2f")


        for _, row in df.iterrows():
            provider_number = row['Phone Number of provider']
            company_name = row['Electrical Company Name']
            company_link = row['URL of the provider']
            renewable_percent=row['Renewable Percentages']
            description=row['Description']

        # Use the company name as the unique key to avoid duplicate entries
            if company_name not in provider_infos:
                provider_info = ProviderInfo(plan_name, company_name, renewable_percent,provider_number, company_link,description,self.new_cost,carbon_emission_savings,cost_savings)
                provider_infos[company_name] = provider_info
            
                if first_provider_info is None:
                    first_provider_info = provider_info

    # Convert back to list of unique provider infos
        return list(provider_infos.values()), first_provider_info


    def get_renewable_percent(self, company):
        """
        Retrieves the renewable percentage of a specific company.
        """
        row = dataset_electric.loc[dataset_electric["Electrical Company Name"] == company]
        if not row.empty:
            return row["Renewable Percentages"].values[0]
        return 0

    def get_peak_off_peak_prices(self, plan_name):
        """
        Retrieves peak and off-peak prices for the given plan.
        """
        unbundled_price = unbundled_df.loc[unbundled_df['Plan'] == plan_name]
        bundled_price = bundled_df.loc[bundled_df['Plan'] == plan_name]

        peak_price = None
        off_peak_price = None

        if not unbundled_price.empty:
            peak_row = unbundled_price[unbundled_price['Type'].str.lower() == 'peak']
            off_peak_row = unbundled_price[unbundled_price['Type'].str.lower() == 'off-peak']
            peak_price = peak_row['Customer Charge Rate'].iloc[0] if not peak_row.empty else None
            off_peak_price = off_peak_row['Customer Charge Rate'].iloc[0] if not off_peak_row.empty else None

        if not bundled_price.empty:
            if peak_price is None:
                peak_row = bundled_price[bundled_price['Type'].str.lower() == 'peak']
                peak_price = peak_row['Customer Charge Rate'].iloc[0] if not peak_row.empty else None
            if off_peak_price is None:
                off_peak_row = bundled_price[bundled_price['Type'].str.lower() == 'off-peak']
                off_peak_price = off_peak_row['Customer Charge Rate'].iloc[0] if not off_peak_row.empty else None

        return peak_price, off_peak_price

    def to_dict(self):
        # Converts recommendations to a dictionary format
        return {
            "current_provider": self.current_provider,
            "recommendations": [rec.to_json() for rec in self.recommendations],
        }



import pandas as pd
from components.electricity.current_price_calculation.current_electricity_cca import Currentelectricity_cca
from steps.provider_info import ProviderInfo

class  electricity_cca:
    def __init__(self, file_path,cost_optimise,carbon_optimise ):
        self.file_path = file_path
        self.df_pge_service = pd.read_excel(file_path, sheet_name='PG&E Service Area')
        self.cca_df = pd.read_excel(file_path, sheet_name='CCA')
        self.jrp_plans_df = pd.read_excel(file_path, sheet_name='Joint Rate Plan')
        self.cost_optimise=cost_optimise
        self.carbon_optimise=carbon_optimise

    def check_pge_cca_service_area(self, zip_code):
        result = self.df_pge_service[self.df_pge_service['PG&E Service area Zip Code'] == zip_code]
        if result.empty:
            return None

        cca_column = []
        for column in self.cca_df.columns:
            if zip_code in self.cca_df[column].values:
                cca_column.append(column)
        if not cca_column:
            return None
        return cca_column

    def get_plans(self, area, user_sector):
        possible_plans = []
        for cca_area in area:
            match = self.jrp_plans_df[self.jrp_plans_df['Location'] == cca_area][['Plan']]
            possible_plans.extend(match['Plan'].tolist())

        sector_plans = []
        for plan in self.jrp_plans_df.itertuples():
            if plan.Sector == user_sector:
                sector_plans.append(plan.Plan)

        return sector_plans

    def fetch_caa_plan_price(self, user_sector, fetched_plans, area):
        prices = []
        plans_list = fetched_plans.split(",")
        for plan in plans_list:
            for location in area:
                price_df = self.jrp_plans_df[
                    (self.jrp_plans_df['Plan'] == plan) &
                    (self.jrp_plans_df['Sector'] == user_sector) &
                    (self.jrp_plans_df['Location'] == location)
                ][['Plan', 'Total Cost', 'Renewable Energy Percentage', 'Electrical Company Name']]

                if not price_df.empty:
                    for _, row in price_df.iterrows():
                        prices.append({
                            "Plan": row["Plan"],
                            "Total Cost": row["Total Cost"],
                            "Renewable Energy percentage": row["Renewable Energy Percentage"],
                            "Electrical Company Name": row["Electrical Company Name"]
                        })

        return prices

    def optimize_plans(self, price):
        # Normalize total cost and renewable energy percentage
        df = pd.DataFrame(price)
        df['Cost Score'] = 1 / df['Total Cost']
        df['Renewable Score'] = df['Renewable Energy percentage']
        df['Combined Score'] = self.cost_optimise * df['Cost Score'] + self.carbon_optimise* df['Renewable Score']  

        best_plan = df.loc[df['Combined Score'].idxmax(), ['Plan', 'Total Cost', 'Electrical Company Name']]

        new_plan_name = best_plan['Plan']
        new_cost = best_plan['Total Cost']
        new_company = best_plan['Electrical Company Name']

        additional_info = self.jrp_plans_df[
            (self.jrp_plans_df['Plan'] == new_plan_name) & 
            (self.jrp_plans_df['Electrical Company Name'] == new_company)
        ][['Phone Number of provider', 'URL of the provider','Renewable Percentages','Description']].iloc[0]

        provider_number = additional_info['Phone Number of provider']
        company_link = additional_info['URL of the provider']
        renewable_percent=additional_info['Renewable Percentages']
        description= additional_info['Description']

        new_info=ProviderInfo(new_plan_name,new_company,renewable_percent,provider_number,company_link,description,new_cost,carbon_emission_savings=0,cost_savings=0)
        return new_plan_name, new_cost, new_company,new_info

    def optimize_renewable(self, price):
        df = pd.DataFrame(price)
        df['Cost Score'] = 1 / df['Total Cost']
        df['Renewable Score'] = df['Renewable Energy percentage']
        df['Combined Score'] = self.cost_optimise * df['Cost Score'] + self.carbon_optimise * df['Renewable Score']

        best_renewable = df.loc[df['Combined Score'].idxmax(), ['Renewable Energy percentage']]

        new_renewable = best_renewable['Renewable Energy percentage']

        return new_renewable

    def get_optimized_plan(self, zip_code, sector):
        area = self.check_pge_cca_service_area(zip_code)
        if area is not None:
            plans = self.get_plans(area, sector)
            final_plans = list(set(plans))
            fetched_plans = ",".join(final_plans)
            price = self.fetch_caa_plan_price(sector, fetched_plans, area)
            final_result,_,_,add_info = self.optimize_plans(price)

            return final_result,add_info
        else:
            return None,None
        
    def get_optimized_plan_cost(self, zip_code, sector,kwh_used):
        area = self.check_pge_cca_service_area(zip_code)
        if area is not None:
            plans = self.get_plans(area, sector)
            final_plans = list(set(plans))
            fetched_plans = ",".join(final_plans)
            price = self.fetch_caa_plan_price(sector, fetched_plans, area)
            final_result = self.optimize_plans(price)
            final_result = final_result[1] * kwh_used
            return final_result
        else:
            return None


    def get_optimized_renewable(self, zip_code, sector):
        area = self.check_pge_cca_service_area(zip_code)
        if area is not None:
            plans = self.get_plans(area, sector)
            final_plans = list(set(plans))
            fetched_plans = ",".join(final_plans)

            price = self.fetch_caa_plan_price(sector, fetched_plans, area)

            final_result = self.optimize_renewable(price)
           
            return final_result
        else:
            return None
        
    
    

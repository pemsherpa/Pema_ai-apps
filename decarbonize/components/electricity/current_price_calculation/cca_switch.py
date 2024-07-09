import pandas as pd

class Currentelectricity_cca:
    def __init__(self, file_path, cost_weight, renewable_weight):
        self.file_path = file_path
        self.cost_weight = user_cost_weight
        self.renewable_weight = user_renewable_weight
        self.df_pge_service = pd.read_excel(file_path, sheet_name='PG&E Service Area')
        self.cca_df = pd.read_excel(file_path, sheet_name='CCA')
        self.jrp_plans_df = pd.read_excel(file_path, sheet_name='Joint Rate Plan')

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

    def optimize_plans(self, price, current_total_cost, current_renewable_percentage):
        # Normalize total cost and renewable energy percentage
        df = pd.DataFrame(price)
        df['Cost Score'] = 1 / df['Total Cost']
        df['Renewable Score'] = df['Renewable Energy percentage']
        df['Combined Score'] = self.cost_weight * df['Cost Score'] + self.renewable_weight * df['Renewable Score']  

        best_plan = df.loc[df['Combined Score'].idxmax(), ['Plan', 'Total Cost', 'Renewable Energy percentage', 'Electrical Company Name']]

        new_plan_name = best_plan['Plan']
        new_cost = best_plan['Total Cost']

        return {
            "New Plan Name": new_plan_name,
            "New Cost": new_cost,
            "New Percentage of Renewable Energy": best_plan['Renewable Energy percentage'],
        }

def get_optimized_plan(file_path, zip_code, sector, company, current_plan_name, current_total_cost, current_renewable_percentage, cost_weight, renewable_weight):
    erp = Currentelectricity_cca(file_path, cost_weight, renewable_weight)
    area = erp.check_pge_cca_service_area(zip_code)
    if area is not None:

        plans = erp.get_plans(area, sector)
        final_plans = list(set(plans))
        fetched_plans = ",".join(final_plans)

        price = erp.fetch_caa_plan_price(sector, fetched_plans, area)
        

        final_result = erp.optimize_plans(price, current_total_cost, current_renewable_percentage)
        return final_result
    else:
        
        return None


final_result = get_optimized_plan(file_path, user_zip_code, user_sector, user_company, user_current_plan, user_current_total_cost, user_current_renewable_percentage, user_cost_weight, user_renewable_weight)
print("Optimization Result:", final_result)

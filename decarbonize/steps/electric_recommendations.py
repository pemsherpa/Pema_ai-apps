import pandas as pd
from steps.quarterly_step import QuaterStep
from steps.electric_decarb_step import ElectricDecarbStep

dataset_electric = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Joint Rate Plan')

class Electric_Recommendations:
    def __init__(self, current_provider, electric_step, cur_year, cur_quarter):
        self.electric_step = electric_step
        self.electric_plan = electric_step.get_new_plan(HasCCA='Yes')
        self.optimized_plan = self.electric_plan

        self.current_provider = current_provider
        self.current_renew_percent = dataset_electric.loc[
            dataset_electric["Electrical Company Name"] == self.current_provider, "Renewable Percentages"].values[0]
        self.new_provider = dataset_electric.loc[dataset_electric["Plan"] == self.optimized_plan, "Electrical Company Name"].tolist()

        self.cur_year = cur_year
        self.cur_quarter = cur_quarter

        self.quarter_steps = []
        self.recommend_plan(1)

    def recommend_plan(self, year):
        if self.current_renew_percent == 100:
            step = QuaterStep(self.cur_year, self.cur_quarter)
            step.add_step()
            self.quarter_steps.append(step)

            return {
                "year": year,
                "recommended_plan": 100,
                "message": "Continue using 100% renewable energy.",
                "New Provider": self.new_provider,
                "carbon_emission_savings": 0
            }

        if year == 1:
            return {
                "year": year,
                "recommended_plan": self.optimized_plan,
                "message": f"Switch to a {self.optimized_plan}% renewable energy source.",
                "New Provider": dataset_electric.loc[
                    dataset_electric["Plan"] == self.optimized_plan, "Electrical Company Name"].tolist(),
                "carbon_emission_savings": self.electric_step.get_electric_carbon_savings()
            }

        if year == 2:
            if self.current_renew_percent < 50:
                new_providers = dataset_electric.loc[
                    (dataset_electric["Renewable Percentages"] >= 50) & 
                    (dataset_electric["Renewable Percentages"] > self.current_renew_percent), 
                    "Electrical Company Name"
                ].tolist()

                return {
                    "year": year,
                    "recommended_plan": 50,
                    "message": "Switch to a plan with at least 50% renewable energy.",
                    "New Provider": new_providers,
                    "carbon_emission_savings": self.electric_step.get_electric_carbon_savings()
                }

            elif 50 <= self.current_renew_percent < 100:
                new_providers = dataset_electric.loc[
                    dataset_electric["Renewable Percentages"] == 100, 
                    "Electrical Company Name"
                ].tolist()

                return {
                    "year": year,
                    "recommended_plan": 100,
                    "message": "Switch to a plan with 100% renewable energy.",
                    "New Provider": new_providers,
                    "carbon_emission_savings":self.electric_step.get_electric_carbon_savings()
                }

        return {
            "year": year,
            "recommended_plan": self.current_renew_percent,
            "message": "Continue with the current plan.",
            "carbon_emission_savings": 0
        }

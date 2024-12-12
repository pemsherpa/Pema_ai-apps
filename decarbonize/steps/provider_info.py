import pandas as pd

unbundled_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Unbundled Peak Time Price')
bundled_df = pd.read_excel('Electricity Rate Plan.xlsx', sheet_name='Bundled Peak Time Price')


class ProviderInfo:
    def __init__(self, plan_name, company, renewable_percent, phone_number, website_link, description,new_cost, carbon_emission_savings, cost_savings):
        self.plan_name = plan_name
        self.company = company
        self.renewable_percent = renewable_percent
        self.phone_number = phone_number
        self.website_link = website_link
        self.description = description
        self.new_cost=new_cost

        # Set the emissions and cost savings directly from the arguments
        self.carbon_savings = carbon_emission_savings
        self.carbon_savings= float(self.carbon_savings)
        self.cost_savings = cost_savings
        self.cost_savings= float(self.cost_savings)

        self.peak, self.off_peak = self.get_peak_off_peak_prices(plan_name)
        self.peak = format(self.peak, ".2f")
        self.peak= float(self.peak)
        self.off_peak = format(self.off_peak, ".2f")
        self.off_peak=float(self.off_peak)

        self.total_cost=format(self.new_cost+self.off_peak+self.peak,".2f")
        self.total_cost=float(self.total_cost)

    def __repr__(self):
        return (f"ProviderInfo(plan_name={self.plan_name}, company_name={self.company}, "
                f"renewable_percent={self.renewable_percent}, provider_number={self.phone_number}, "
                f"company_link={self.website_link}, description={self.description}, "
                f"Carbon savings={self.carbon_savings}, Cost savings={self.cost_savings}, "
                f"Peak Cost={self.peak}, Off-Peak Cost={self.off_peak}), total_cost={self.total_cost}")

    def to_dict(self):
        return {
            "plan_name": self.plan_name,
            "company": self.company,
            "renewable percent provided": self.renewable_percent,
            "phone_number": self.phone_number,
            "website_link": self.website_link,
            "description of the company": self.description,
            "Carbon savings": self.carbon_savings,
            "Cost savings": self.cost_savings,
            "Peak Cost": self.peak,
            "Off-Peak Cost": self.off_peak,
            "Total-Cost_with_peak_and_off-peak":self.total_cost
        }
    
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


    
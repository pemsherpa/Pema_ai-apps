class ProviderInfoCru:
    def __init__(self, company, phone_number, website_link, description,provider_type, carbon_emission_savings, cost_savings,location,new_cost):
        self.company = company
        self.phone_number = phone_number
        self.website_link = website_link
        self.description = description
        self.provider_type = provider_type
        self.location = location
        self.new_cost=new_cost

        # Set the emissions and cost savings directly from the arguments
        self.carbon_savings = carbon_emission_savings
        self.cost_savings = cost_savings

    def __repr__(self):
        return (f"ProviderInfoCru(company_name={self.company}, provider_number={self.phone_number}, "
                f"company_link={self.website_link}, description={self.description},type={self.provider_type}, "
                f"Carbon savings={self.carbon_savings}, Cost savings={self.cost_savings}, Location={self.location}), Total-Cost={self.new_cost}")

    def to_dict(self):
        return {
            "plan_name":"Purchase of carbon cerdits",
            "company": self.company,
            "renewable percent provided": None,
            "phone_number": self.phone_number,
            "website_link": self.website_link,
            "description of the company": self.description,
            "location":self.location,
            "Carbon savings": self.carbon_savings,
            "Cost savings": self.cost_savings,
            "Peak Cost": None,
            "Off-Peak Cost":None, 
            "Total-Cost":self.new_cost}


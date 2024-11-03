class ProviderInfoCru:
    def __init__(self, company, phone_number, website_link, description,provider_type, carbon_emission_savings, cost_savings,location):
        self.company = company
        self.phone_number = phone_number
        self.website_link = website_link
        self.description = description
        self.provider_type = provider_type
        self.location = location

        # Set the emissions and cost savings directly from the arguments
        self.carbon_savings = carbon_emission_savings
        self.cost_savings = cost_savings

    def __repr__(self):
        return (f"ProviderInfoCru(company_name={self.company}, provider_number={self.phone_number}, "
                f"company_link={self.website_link}, description={self.description},type={self.provider_type}, "
                f"Carbon savings={self.carbon_savings}, Cost savings={self.cost_savings}, Location={self.location})")

    def to_dict(self):
        return {
            "company": self.company,
            "phone_number": self.phone_number,
            "website_link": self.website_link,
            "company_description": self.description,
            "type":self.provider_type,
            "location":self.location,
            "carbon_savings": self.carbon_savings,
            "cost_savings": self.cost_savings
        }

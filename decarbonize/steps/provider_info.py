class ProviderInfo:
    def __init__(self, plan_name, company, renewable_percent, phone_number, website_link,description):
        self.plan_name = plan_name
        self.company = company
        self.renewable_percent=renewable_percent,
        self.phone_number = phone_number
        self.website_link = website_link
        self.description= description

    def __repr__(self):
        return (f"ProviderInfo(plan_name={self.plan_name}, company_name={self.company},renewable_percent={self.renewable_percent} "
                f"provider_number={self.phone_number}, company_link={self.website_link}, description={self.description})")
    
    def to_dict(self):
        return {
            "plan_name": self.plan_name,
            "company": self.company,
            "renewable percent provided":self.renewable_percent,
            "phone_number": self.phone_number,
            "website_link": self.website_link,
            "description of the company": self.description
        }


    
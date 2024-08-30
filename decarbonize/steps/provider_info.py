class ProviderInfo():
    def __init__(self,plan_name,company,phone_number,website_link):
        self.plan_name=plan_name
        self.company=company
        self.phone_number=phone_number
        self.website_link=website_link

    def __repr__(self):
        return (f"ProviderInfo(plan_name={self.plan_name}, company_name={self.company}, "
                f"provider_number={self.phone_number}, company_link={self.website_link})")

    
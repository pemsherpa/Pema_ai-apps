class CRU_Recommendation:
    def __init__(self, year, recommended_plan, message, carbon_emission_savings, cost_savings, provider_info, first_provider_info):
        self.year = year
        self.recommended_plan = recommended_plan
        self.message = message
        self.carbon_emission_savings = carbon_emission_savings
        self.cost_savings = cost_savings
        self.provider_info = provider_info
        self.first_provider_info = first_provider_info

    def to_json(self):
        # Assuming provider_info and first_provider_info are objects with attributes you want to serialize
        return {
            "recommended_plan": self.recommended_plan,
            "message": self.message,
            "carbon_emission_savings": self.carbon_emission_savings,
            "cost_savings": self.cost_savings,
            "provider_info": self.provider_info,
            #     "company": self.provider_info.company,
            #     "mobile": self.provider_info.phone_number,
            #     "website": self.provider_info.website_link
            # },
            "our_recommendation": self.first_provider_info
                # "mobile": self.first_provider_info.phone_number,
                # "website": self.first_provider_info.website_link
        }

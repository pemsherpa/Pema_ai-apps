class Electric_Recommendation:
    def __init__(self, year, recommended_plan, message, carbon_emission_savings, provider_info):
        self.year = year
        self.recommended_plan = recommended_plan
        self.message = message
        self.carbon_emission_savings = carbon_emission_savings
        self.provider_info = provider_info
    
    def to_json(self):
        return {
            "year": self.year,
            "recommended_plan": self.recommended_plan,
            "message": self.message,
            "carbon_emission_savings": self.carbon_emission_savings,
            "provider_info": self.provider_info
        }
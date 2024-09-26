class Electric_Recommendation:
    def __init__(self, recommended_plan, message, carbon_emission_savings,cost_savings,peak,off_peak, provider_info,first_provider_info):
        self.recommended_plan = recommended_plan
        self.message = message
        self.carbon_emission_savings = carbon_emission_savings
        self.cost_savings=cost_savings
        self.peak=peak
        self.off_peak=off_peak
        self.provider_info = provider_info
        self.first_provider_info=first_provider_info
    
    def to_json(self):
        return {
            "recommended_plan": self.recommended_plan,
            "message": self.message,
            "carbon_emission_savings": self.carbon_emission_savings,
            "cost savings":self.cost_savings,
            "peak":self.peak,
            "off_peak":self.off_peak,
            "provider_info": self.provider_info,
            "our recommendation":self.first_provider_info
        }
class Electric_Recommendation:
    def __init__(self, recommended_plan, message, provider_info,first_provider_info):
        self.recommended_plan = recommended_plan
        self.message = message
        self.provider_info = provider_info
        self.first_provider_info=first_provider_info
    
    def to_json(self):
        return {
            "recommended_plan": self.recommended_plan,
            "message": self.message,
            "provider_info": self.provider_info,
            "our recommendation":self.first_provider_info
        }
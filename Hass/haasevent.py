

class HaasEvent:
    def __init__(self,estimated_attance, name, location, time):
        self.min_attendance = estimated_attance[0]
        self.max_attendance = estimated_attance[1]
        self.mean_attance = (self.min_attendance + self.max_attendance) // 2

        self.ci_distribution = [self.min_attendance*.8, self.max_attendance*1.2]
        self.name = name
        self.location=location
        self.time = time
    
    def save_emissions(self, emissions_student_obj, emissions_nonstudent_obj):
        self.emissions_student_obj = emissions_student_obj
        self.emissions_nonstudent_obj = emissions_nonstudent_obj

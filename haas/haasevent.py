

class HaasEvent:
    def __init__(self,estimated_attendance, student, non_student, location, time):
        self.min_attendance = estimated_attendance[0]
        self.max_attendance = estimated_attendance[1]
        self.mean_attendance = (self.min_attendance + self.max_attendance) // 2
        
        self.student_percentage = student
        self.non_student_percentage = non_student

        self.ci_distribution = [self.min_attendance*.8, self.max_attendance*1.2]
        #self.name = name excelsheet does not have name
        self.location=location
        self.time = time

        self.student_attendance = self.student_percentage * self.mean_attendance
        self.non_student_attendance = self.non_student_percentage * self.mean_attendance

    
    def save_emissions(self, emissions_student_obj, emissions_nonstudent_obj):
        self.emissions_student_obj = emissions_student_obj
        self.emissions_nonstudent_obj = emissions_nonstudent_obj

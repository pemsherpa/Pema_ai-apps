
class DecarbWeight:
    def __init__(self, price_weight, duration_weight,stop_weight,carbon_weight):
        self.price_weight =price_weight
        self.duration_weight = duration_weight
        self.stop_weight = stop_weight
        self.carbon_weight = carbon_weight
        if not self.verify_weight():

          raise ValueError("Weight must add up to 1")
    def verify_weight(self):
      lst = [self.price_weight,self.duration_weight,self.stop_weight,self.carbon_weight]

      total = sum(lst)
      
      return round(total,2)==1

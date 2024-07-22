
class Sector_simplified:     
    
    def __init__(self):
        pass

    def get_usage_dict(self, peak_range, part_peak_range, peak_usage, part_peak_usage, off_peak_usage, super_off_peak_range=[], superoff_peak_usage=None ):
        usage_dict = {}
        for hour in range(24):
            if hour in peak_range:
                usage_dict[f'{hour}_oclock_usage'] = peak_usage.usage / peak_usage.hours
            elif hour in part_peak_range:
                usage_dict[f'{hour}_oclock_usage'] = part_peak_usage.usage / part_peak_usage.hours
            elif hour in super_off_peak_range:
                usage_dict[f'{hour}_oclock_usage'] = superoff_peak_usage.usage / superoff_peak_usage.hours
            else:
                usage_dict[f'{hour}_oclock_usage'] = off_peak_usage.usage / off_peak_usage.hours
        return usage_dict

class ElectricUsage:     
    
    def __init__(self, usage, hours):
        self. usage = usage
        self. hours = hours

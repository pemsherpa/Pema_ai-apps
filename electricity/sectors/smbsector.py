
class SMBSector:
    def __init__(self, A1NTBStotal_usage, A1NTBWtotal_usage, A1BSpeak_usage,
                 A1BSpartpeak_usage, A1BSoffpeak_usage, A1BWpartpeak_usage,
                 A1BWoffpeak_usage, B1BSpeak_usage, B1BSpartpeak_usage, B1BSoffpeak_usage,
                 B1BWpeak_usage, B1BWsuperoffpeak_usage, B1BWoffpeak_usage,
                 B1STBSpeak_usage, B1STBSpartpeak_usage, B1STBSoffpeak_usage,
                 B1STBWpeak_usage, B1STBWpartpeak_usage, B1STBWsuperoffpeak_usage,
                 B1STBWoffpeak_usage, B6BSpeak_usage, B6BSoffpeak_usage,
                 B6BWpeak_usage, B6BWsuperoffpeak_usage,B6BWoffpeak_usage,
                 B10SVBSpeak_usage,B10SVBSpartpeak_usage,B10SVBSoffpeak_usage,
                 B10SVBWpeak_usage, B10SVBWsuperoffpeak_usage, B10SVBWoffpeak_usage,
                 B10PVBSpeak_usage,B10PVBSpartpeak_usage,B10PVBSoffpeak_usage,
                 B10PVBWpeak_usage,B10PVBWsuperoffpeak_usage,B10PVBWoffpeak_usage,
                 B10TVBSpeak_usage, B10TVBSpartpeak_usage,B10TVBSoffpeak_usage,
                 B10TVBWpeak_usage,B10TVBWsuperoffpeak_usage, B10TVBWoffpeak_usage,
                 meter_input,time_in_use, max_15min_usage,B1STB_highest_demand_15mins):
        self.A1NTBStotal_usage = A1NTBStotal_usage
        self.A1NTBWtotal_usage = A1NTBWtotal_usage
        self.A1BSpeak_usage = A1BSpeak_usage
        self.A1BSpartpeak_usage = A1BSpartpeak_usage
        self.A1BSoffpeak_usage = A1BSoffpeak_usage
        self.A1BWpartpeak_usage = A1BWpartpeak_usage 
        self.A1BWoffpeak_usage = A1BWoffpeak_usage
        self.B1BSpeak_usage = B1BSpeak_usage
        self.B1BSpartpeak_usage = B1BSpartpeak_usage
        self.B1BSoffpeak_usage = B1BSoffpeak_usage
        self.B1BWpeak_usage = B1BWpeak_usage
        self.B1BWsuperoffpeak_usage = B1BWsuperoffpeak_usage
        self.B1BWoffpeak_usage = B1BWoffpeak_usage
        self.B1STBSpeak_usage = B1STBSpeak_usage
        self.B1STBSpartpeak_usage = B1STBSpartpeak_usage
        self.B1STBSoffpeak_usage = B1STBSoffpeak_usage
        self.B1STBWpeak_usage = B1STBWpeak_usage
        self.B1STBWpartpeak_usage = B1STBWpartpeak_usage
        self.B1STBWsuperoffpeak_usage = B1STBWsuperoffpeak_usage
        self.B1STBWoffpeak_usage = B1STBWoffpeak_usage
        self.B6BSpeak_usage = B6BSpeak_usage
        self.B6BSoffpeak_usage = B6BSoffpeak_usage
        self.B6BWpeak_usage = B6BWpeak_usage
        self.B6BWsuperoffpeak_usage = B6BWsuperoffpeak_usage
        self.B6BWoffpeak_usage = B6BWoffpeak_usage
        self.B10SVBSpeak_usage = B10SVBSpeak_usage
        self.B10SVBSpartpeak_usage = B10SVBSpartpeak_usage
        self.B10SVBSoffpeak_usage = B10SVBSoffpeak_usage
        self.B10SVBWpeak_usage = B10SVBWpeak_usage
        self.B10SVBWsuperoffpeak_usage = B10SVBWsuperoffpeak_usage
        self.B10SVBWoffpeak_usage = B10SVBWoffpeak_usage
        self.B10PVBSpeak_usage = B10PVBSpeak_usage
        self.B10PVBSpartpeak_usage = B10PVBSpartpeak_usage
        self.B10PVBSoffpeak_usage = B10PVBSoffpeak_usage
        self.B10PVBWpeak_usage = B10PVBWpeak_usage
        self.B10PVBWsuperoffpeak_usage = B10PVBWsuperoffpeak_usage
        self.B10PVBWoffpeak_usage = B10PVBWoffpeak_usage
        self.B10TVBSpeak_usage = B10TVBSpeak_usage
        self.B10TVBSpartpeak_usage = B10TVBSpartpeak_usage
        self.B10TVBSoffpeak_usage = B10TVBSoffpeak_usage
        self.B10TVBWpeak_usage = B10TVBWpeak_usage
        self.B10TVBWsuperoffpeak_usage = B10TVBWsuperoffpeak_usage
        self.B10TVBWoffpeak_usage = B10TVBWoffpeak_usage
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage
        self.B1STB_highest_demand_15mins = B1STB_highest_demand_15mins

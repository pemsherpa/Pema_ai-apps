class LCBSector:
    def __init__(self, B19SVBSpeak_usage, B19SVBSpartpeak_usage, B19SVBSoffpeak_usage,
                 B19SVBWpeak_usage,B19SVBWsuperoffpeak_usage,B19SVBWoffpeak_usage,
                 B19PVBSpeak_usage,B19PVBSpartpeak_usage,B19PVBSoffpeak_usage,
                 B19PVBWpeak_usage,B19PVBWsuperoffpeak_usage,B19PVBWoffpeak_usage,
                 B19TVBSpeak_usage,B19TVBSpartpeak_usage,B19TVBSoffpeak_usage,
                 B19TVBWpeak_usage,B19TVBWsuperoffpeak_usage,B19TVBWoffpeak_usage,
                 B20SVBSpeak_usage, B20SVBSpartpeak_usage, B20SVBSoffpeak_usage,
                 B20SVBWpeak_usage,B20SVBWsuperoffpeak_usage,B20SVBWoffpeak_usage,
                 B20PVBSpeak_usage,B20PVBSpartpeak_usage,B20PVBSoffpeak_usage,
                 B20PVBWpeak_usage,B20PVBWsuperoffpeak_usage,B20PVBWoffpeak_usage,
                 B20TVBSpeak_usage,B20TVBSpartpeak_usage,B20TVBSoffpeak_usage,
                 B20TVBWpeak_usage,B20TVBWsuperoffpeak_usage,B20TVBWoffpeak_usage,
                 meter_input,time_in_use,max_15min_usage):
        self.B19SVBSpeak_usage = B19SVBSpeak_usage
        self.B19SVBSpartpeak_usage = B19SVBSpartpeak_usage
        self.B19SVBSoffpeak_usage = B19SVBSoffpeak_usage
        self.B19SVBWpeak_usage = B19SVBWpeak_usage
        self.B19SVBWsuperoffpeak_usage = B19SVBWsuperoffpeak_usage
        self.B19SVBWoffpeak_usage = B19SVBWoffpeak_usage
        self.B19PVBSpeak_usage = B19PVBSpeak_usage
        self.B19PVBSpartpeak_usage = B19PVBSpartpeak_usage
        self.B19PVBSoffpeak_usage = B19PVBSoffpeak_usage
        self.B19PVBWpeak_usage = B19PVBWpeak_usage
        self.B19PVBWsuperoffpeak_usage = B19PVBWsuperoffpeak_usage
        self.B19PVBWoffpeak_usage = B19PVBWoffpeak_usage
        self.B19TVBSpeak_usage = B19TVBSpeak_usage
        self.B19TVBSpartpeak_usage = B19TVBSpartpeak_usage
        self.B19TVBSoffpeak_usage = B19TVBSoffpeak_usage
        self.B19TVBWpeak_usage = B19TVBWpeak_usage
        self.B19TVBWsuperoffpeak_usage = B19TVBWsuperoffpeak_usage
        self.B19TVBWoffpeak_usage = B19TVBWoffpeak_usage
        self.B20SVBSpeak_usage = B20SVBSpeak_usage
        self.B20SVBSpartpeak_usage = B20SVBSpartpeak_usage
        self.B20SVBSoffpeak_usage = B20SVBSoffpeak_usage
        self.B20SVBWpeak_usage = B20SVBWpeak_usage
        self.B20SVBWsuperoffpeak_usage = B20SVBWsuperoffpeak_usage
        self.B20SVBWoffpeak_usage = B20SVBWoffpeak_usage
        self.B20PVBSpeak_usage = B20PVBSpeak_usage
        self.B20PVBSpartpeak_usage = B20PVBSpartpeak_usage
        self.B20PVBSoffpeak_usage = B20PVBSoffpeak_usage
        self.B20PVBWpeak_usage = B20PVBWpeak_usage
        self.B20PVBWsuperoffpeak_usage = B20PVBWsuperoffpeak_usage
        self.B20PVBWoffpeak_usage = B20PVBWoffpeak_usage
        self.B20TVBSpeak_usage = B20TVBSpeak_usage
        self.B20TVBSpartpeak_usage = B20TVBSpartpeak_usage
        self.B20TVBSoffpeak_usage = B20TVBSoffpeak_usage
        self.B20TVBWpeak_usage = B20TVBWpeak_usage
        self.B20TVBWsuperoffpeak_usage = B20TVBWsuperoffpeak_usage
        self.B20TVBWoffpeak_usage = B20TVBWoffpeak_usage
        self.meter_input = meter_input
        self.time_in_use = time_in_use
        self.max_15min_usage = max_15min_usage

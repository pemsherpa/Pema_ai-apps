
class SMBSector:
    def __init__(self, A1NTBStotal_usage, A1NTBWtotal_usage, A1BSpeak_usage):
        self.A1NTBStotal_usage = A1NTBStotal_usage
        self.A1NTBWtotal_usage = A1NTBWtotal_usage
        self.A1BSpeak_usage = A1BSpeak_usage
        # TODO Jinduo please complete


usage_data = {
    'A1NTBStotal_usage': ...,  # User provided
    'A1NTBWtotal_usage': ...,  # User provided
    'A1BSpeak_usage': ...,  # User provided
    'A1BSpartpeak_usage': ...,  # User provided
    'A1BSoffpeak_usage': ...,  # User provided
    'A1BWpartpeak_usage': ...,  # User provided
    'A1BWoffpeak_usage': ...,  # User provided
    'B1BSpeak_usage': ...,  # User provided
    'B1BSpartpeak_usage': ...,  # User provided
    'B1BSoffpeak_usage': ...,  # User provided
    'B1BWpeak_usage': ...,  # User provided
    'B1BWsuperoffpeak_usage': ...,  # User provided
    'B1BWoffpeak_usage': ...,  # User provided
    'B1STBSpeak_usage': ...,  # User provided
    'B1STBSpartpeak_usage': ...,  # User provided
    'B1STBSoffpeak_usage': ...,  # User provided
    'B1STBWpeak_usage': ...,  # User provided
    'B1STBWpartpeak_usage': ...,  # User provided
    'B1STBWsuperoffpeak_usage': ...,  # User provided
    'B1STBWoffpeak_usage': ...,  # User provided
    'B6BSpeak_usage': ...,  # User provided
    'B6BSoffpeak_usage': ...,  # User provided
    'B6BWpeak_usage': ...,  # User provided
    'B6BWsuperoffpeak_usage': ...,  # User provided
    'B6BWoffpeak_usage': ...,  # User provided
    'B10SVBSpeak_usage': ...,  # User provided
    'B10SVBSpartpeak_usage': ...,  # User provided
    'B10SVBSoffpeak_usage': ...,  # User provided
    'B10SVBWpeak_usage': ...,  # User provided
    'B10SVBWsuperoffpeak_usage': ...,  # User provided
    'B10SVBWoffpeak_usage': ...,  # User provided
    'B10PVBSpeak_usage': ...,  # User provided
    'B10PVBSpartpeak_usage': ...,  # User provided
    'B10PVBSoffpeak_usage': ...,  # User provided
    'B10PVBWpeak_usage': ...,  # User provided
    'B10PVBWsuperoffpeak_usage': ...,  # User provided
    'B10PVBWoffpeak_usage': ...,  # User provided
    'B10TVBSpeak_usage': ...,  # User provided
    'B10TVBSpartpeak_usage': ...,  # User provided
    'B10TVBSoffpeak_usage': ...,  # User provided
    'B10TVBWpeak_usage': ...,  # User provided
    'B10TVBWsuperoffpeak_usage': ...,  # User provided
    'B10TVBWoffpeak_usage': ...,  # User provided
    'meter_input': ...,  # User provided
    'time_in_use': ...,  # User provided
    'max_15min_usage': ...,  # User provided
    'B1STB_highest_demand_15mins': ...,  # User provided
}
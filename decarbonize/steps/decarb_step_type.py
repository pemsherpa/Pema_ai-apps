from enum import Enum

class DecarbStepType(Enum):
    FLIGHTS = 1
    COMMUTING = 2
    ELECTRICITY = 3

DecarbStepType = Enum('DecarbStepType', ['FLIGHTS', 'COMMUTING', 'ELECTRICITY'])

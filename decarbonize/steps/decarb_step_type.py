from enum import Enum

from enum import Enum, auto

class DecarbStepType(Enum):
    COMMUTING_INDIVIDUAL = auto()
    COMMUTING_CARPOOL = auto()
    FLIGHTS = auto()
    FLIGHTS_RETURN = auto()
    FLIGHT_OPTIMIZER = auto()
    ELECTRICITY = auto()
    ELECTRICITY_ANNUAL = auto()
    CRU = auto()
    CRU_ANNUAL=auto()

    def __str__(self) -> str:
        return self.name
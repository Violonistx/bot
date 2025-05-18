from enum import Enum, auto

class BookingStates(Enum):
    SELECT_EVENT = auto()
    NAME = auto()
    PHONE = auto()
    TIME = auto()

class EventStates(Enum):
    NAME = auto()
    PHONE = auto()
    COMMENT = auto()
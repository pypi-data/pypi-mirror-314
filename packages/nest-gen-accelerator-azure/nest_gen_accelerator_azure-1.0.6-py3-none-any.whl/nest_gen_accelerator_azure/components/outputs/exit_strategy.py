from enum import Enum


class ExitStrategy(Enum):
    # System-wide
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"
    EMPTY = ""
    ON_ERROR = "ON_ERROR"
    CONVERSATION_STALLED = "CONVERSATION_STALLED"

    # Module-specific
    ORDER = "ORDER"
    ACCOUNT = "ACCOUNT"
    PROMOTIONS = "PROMOTIONS"
    MACHINE = "MACHINE"

import enum

class InteractionType(enum.Enum):
    CHECK = 1
    HINT = 2
    SOLUTION = 3

class OutcomeType(enum.Enum):
    PASS = 1
    FAIL = 2
    EXCEPTION = 3
    UNATTEMPTED = 4

def track(event):
    pass

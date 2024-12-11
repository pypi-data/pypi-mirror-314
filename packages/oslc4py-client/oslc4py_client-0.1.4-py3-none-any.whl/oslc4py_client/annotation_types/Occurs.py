from enum import Enum

class Occurs(Enum):
    EXACTLY_ONE = "ExactlyOne"
    ONE_OR_MANY = "OneOrMany"
    ZERO_OR_MANY = "ZeroOrMany"
    ZERO_OR_ONE = "ZeroOrOne"
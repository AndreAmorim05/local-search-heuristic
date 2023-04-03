from dataclasses import dataclass
from enum import Enum


class Risk(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


@dataclass
class Investiment:
    """
    Class that represents an investiment
    """
    description: str
    cost: float
    recovery: float
    risk: Risk
    score: float = None

    def __post_init__(self):
        self.score = self.recovery / self.cost

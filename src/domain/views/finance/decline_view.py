from dataclasses import dataclass


@dataclass
class DeclineView:
    decline_code: int
    bank_name: str
    occurrence: int = 0


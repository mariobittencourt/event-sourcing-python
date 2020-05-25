from dataclasses import dataclass


@dataclass
class DeclineView:
    decline_code: int
    bank_name: str
    date: str
    count: int = 0


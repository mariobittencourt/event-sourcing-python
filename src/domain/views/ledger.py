class Ledger:
    def __init__(self, ledger_id: int, projection_name: str, last_position: int = -1):
        self.ledger_id = ledger_id
        self.projection_name = projection_name
        self.last_position = last_position

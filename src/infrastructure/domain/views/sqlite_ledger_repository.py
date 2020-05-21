import sqlite3
from typing import Optional

from src.domain.views.ledger import Ledger
from src.domain.views.ledger_repository import LedgerRepository


class SqliteLedgerRepository(LedgerRepository):
    def __init__(self, database_name: str) -> None:
        self._connection = sqlite3.connect(database_name)
        self._connection.row_factory = sqlite3.Row

    def initialize(self) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute('''CREATE TABLE ledger
                         (ledger_id INTEGER PRIMARY KEY AUTOINCREMENT, projection_name text, last_position int)''')
            cursor.execute('CREATE UNIQUE INDEX idx_ledger_projection_name ON ledger (projection_name)')
        except sqlite3.OperationalError:
            # this would have to see if the table already exists to pass
            pass
        return True

    def update(self, ledger: Ledger) -> bool:
        cursor = self._connection.cursor()
        cursor.execute('UPDATE ledger SET last_position=? WHERE ledger_id=?',
                       (ledger.last_position, ledger.ledger_id))
        self._connection.commit()
        return True

    def insert(self, ledger: Ledger) -> bool:
        cursor = self._connection.cursor()
        cursor.execute('INSERT INTO ledger VALUES (?,?)',
                       ((ledger.projection_name,), ledger.last_position))
        self._connection.commit()
        return True

    def find_by_id(self, ledger_id: int) -> Optional[Ledger]:
        cursor = self._connection.cursor()
        cursor.execute('SELECT * FROM ledger WHERE ledger_id = ?', (ledger_id,))
        row = cursor.fetchone()
        if row is not None:
            ledger = Ledger(
                ledger_id=row['ledger_id'],
                projection_name=row['projection_name'],
                last_position=row['last_position']
            )
            return ledger

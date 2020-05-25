import sqlite3
from typing import List

from src.domain.views.finance.decline_view import DeclineView
from src.domain.views.finance.decline_view_repository import DeclineViewRepository


class SqliteDeclineViewRepository(DeclineViewRepository):
    def __init__(self, database_name: str) -> None:
        self._connection = sqlite3.connect(database_name)
        self._connection.row_factory = sqlite3.Row

    def initialize(self) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute('''CREATE TABLE decline_view
                         (decline_code int, bank_name text, date text, count int default 1)''')
            cursor.execute('CREATE UNIQUE INDEX idx_decline_view ON decline_view (decline_code, bank_name, date)')
            cursor.execute('CREATE INDEX idx_decline_view_decline_code ON decline_view (decline_code, date)')
        except sqlite3.OperationalError:
            # this would have to see if the table already exists to pass
            pass
        return True

    def reset(self) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute('TRUNCATE TABLE decline_view')
            self._connection.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def increment_occurrence(self, decline_code: int, bank_name: str, date: str) -> bool:
        cursor = self._connection.cursor()
        cursor.execute('INSERT INTO decline_view(decline_code, bank_name, date, count) VALUES(?,?,?,1) ON CONFLICT(decline_code, bank_name, date) DO UPDATE SET count=count+1',
                       (decline_code, bank_name, date))
        self._connection.commit()
        return True

    def find_by_decline_code(self, decline_code: int) -> List[DeclineView]:
        cursor = self._connection.cursor()
        cursor.execute('SELECT * FROM decline_view WHERE decline_code = ? ORDER BY date ASC', (decline_code,))
        # in practice paginate
        result = []
        for row in cursor.fetchall():
            if row is not None:
                result.append(
                    DeclineView(
                        decline_code=row['decline_code'],
                        bank_name=row['bank_name'],
                        date=row['date'],
                        count=row['count']
                    )
                )
        return result

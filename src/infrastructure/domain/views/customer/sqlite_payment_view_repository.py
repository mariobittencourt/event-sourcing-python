import sqlite3
from typing import Optional

from src.domain.views.customer.payment_view import PaymentView
from src.domain.views.customer.payment_view_repository import PaymentViewRepository


class SqlitePaymentViewRepository(PaymentViewRepository):
    def __init__(self, database_name: str) -> None:
        self._connection = sqlite3.connect(database_name)
        self._connection.row_factory = sqlite3.Row

    def initialize(self) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute('''CREATE TABLE payment_view
                         (payment_id text, status text, amount_due real, last_updated_at text)''')
            cursor.execute('CREATE UNIQUE INDEX idx_payment_view_payment_id ON payment_view (payment_id)')
        except sqlite3.OperationalError:
            # this would have to see if the table already exists to pass
            pass
        return True

    def reset(self) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute('TRUNCATE TABLE payment_view')
            self._connection.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def update(self, payment: PaymentView) -> bool:
        cursor = self._connection.cursor()
        cursor.execute('UPDATE payment_view SET status=?, amount_due=?, last_updated_at=? WHERE payment_id=?',
                       (payment.status, payment.amount_due, payment.last_updated_at, payment.payment_id))
        self._connection.commit()
        return True

    def insert(self, payment: PaymentView) -> bool:
        cursor = self._connection.cursor()
        cursor.execute('INSERT INTO payment_view VALUES (?,?,?,?)',
                       (payment.payment_id, payment.status, payment.amount_due, payment.last_updated_at))
        self._connection.commit()
        return True

    def find_by_id(self, payment_id: str) -> Optional[PaymentView]:
        cursor = self._connection.cursor()
        cursor.execute('SELECT * FROM payment_view WHERE payment_id = ?', (payment_id,))
        row = cursor.fetchone()
        if row is not None:
            payment = PaymentView(
                payment_id=row['payment_id'],
                status=row['status'],
                amount_due=row['amount_due'],
                last_updated_at=row['last_updated_at'])
            return payment

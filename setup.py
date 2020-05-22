import getopt
import sys

from src.config.settings import DATABASE_NAME
from src.domain.views.ledger import Ledger
from src.infrastructure.domain.views.sqlite_ledger_repository import SqliteLedgerRepository
from src.infrastructure.domain.views.sqlite_payment_view_repository import SqlitePaymentViewRepository

if __name__ == "__main__":
    # Create ledger to hold the progress
    ledger_repository = SqliteLedgerRepository(database_name=DATABASE_NAME)
    if ledger_repository.initialize():
        print('Ledger persistence available')

    # Create the payment projection view
    payment_view_repository = SqlitePaymentViewRepository(database_name=DATABASE_NAME)
    if payment_view_repository.initialize():
        print('Payment projection available')

    opts, args = getopt.getopt(sys.argv[1:], 'r', ["reset"])
    for o, a in opts:
        if o in ('-r', '--reset'):
            payment_view_repository.reset()
            ledger_repository.reset()
            print('Persistence reset')
        else:
            assert False, 'Unknown option'

    ledger_repository.insert(Ledger(1, 'payment'))

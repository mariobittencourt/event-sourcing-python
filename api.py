from optparse import OptionParser
import asyncio

from src.config.settings import EVENT_STORE_PASSWORD, EVENT_STORE_USERNAME
from src.domain.models.invalid_state_error import InvalidStateError
from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId
from src.infrastructure.domain.models.event_store_payment_repository import EventStorePaymentRepository


async def save(my_payment: Payment):
    repository = EventStorePaymentRepository(username=EVENT_STORE_USERNAME, password=EVENT_STORE_PASSWORD)
    await repository.save(my_payment)


async def find(my_payment_id: str):
    repository = EventStorePaymentRepository(username=EVENT_STORE_USERNAME, password=EVENT_STORE_PASSWORD)
    return await repository.find_by_id(PaymentId(my_payment_id))


def print_payment(my_payment: Payment):
    print(f'ID: {my_payment.payment_id}')
    print(f'Status: {my_payment.status.value}')
    print(f'Amount due: {my_payment.amount_due}')
    print(f'Transactions:')
    for transaction in my_payment.transactions:
        print(transaction)
        print('\t-----------------------')


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-a', action='store', help='Which action to execute create, authorize, settle, decline, refund or find')
    parser.add_option('-i', action='store', help='The customer ID to authorize, settle, decline, refund or find')
    parser.add_option('-v', action='store', help='The amount to create, settle or refund', default=100.00)
    parser.add_option('-b', action='store', help='The bank name', default='My Super Bank')
    parser.add_option('-c', action='store', help='The reason code for declines', default=999)

    (options, args) = parser.parse_args()
    amount = float(options.v)
    payment_id = options.i
    bank_name = options.b
    decline_code = options.c

    loop = asyncio.get_event_loop()
    if options.a == 'create':
        payment = Payment.create(PaymentId(), amount)
        loop.run_until_complete(save(payment))
        print_payment(payment)
    else:
        payment = loop.run_until_complete(find(payment_id))
        if payment is None:
            print('Payment not found')
            exit(0)

        if options.a == 'find':
            print_payment(payment)
            exit(0)

        try:
            if options.a == 'authorize':
                payment.authorize(bank_name, 'xxx-uuu-id')
            elif options.a == 'settle':
                payment.settle(bank_name=bank_name, amount_settled=amount, settlement_id='xxx-zzz-id')
            elif options.a == 'decline':
                payment.decline(bank_name=bank_name, decline_code=decline_code, decline_id='zzz-uuu-id')
            elif options.a == 'refund':
                payment.refund(amount_refunded=amount, refund_id='1-800-GOT-JUNK')

            loop.run_until_complete(save(payment))
            print_payment(payment)
        except InvalidStateError as exception:
            print(f'Unable to perform the requested operation: {exception}')


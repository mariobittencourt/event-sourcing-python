import asyncio
import photonpump

from src.domain.models.payment import Payment
from src.domain.models.payment_authorized import PaymentAuthorized
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_declined import PaymentDeclined
from src.domain.models.payment_id import PaymentId
from src.domain.models.payment_refunded import PaymentRefunded
from src.domain.models.payment_repository import PaymentRepository
from src.domain.models.payment_settled import PaymentSettled


class EventStorePaymentRepository(PaymentRepository):
    def __init__(self, username: str, password: str):
        self._loop = asyncio.get_event_loop()
        self._client = photonpump.connect(loop=self._loop, username=username, password=password)
        self._connected = False

    async def save(self, payment: Payment) -> bool:
        await self._check_connection()

        stream_name = self._create_stream_name(payment.payment_id)
        for event in payment.events:
            # We could publish in batches
            await self._client.publish_event(stream_name, event.type, event.encode())

        return True

    async def _check_connection(self):
        if not self._connected:
            await self._client.connect()
            self._connected = True

    def _create_stream_name(self, payment_id: PaymentId) -> str:
        return f'payment-{payment_id.value}'

    async def find_by_id(self, payment_id: PaymentId) -> Payment:
        await self._check_connection()

        stream_name = self._create_stream_name(payment_id)
        payment = Payment(payment_id)
        async for event in self._client.iter(stream=stream_name, from_event=0):
            await self._reconstruct_from_event(event, payment)

        # I clear the events so changes won't multiply the events themselves
        payment.clear_events()

        return payment

    async def _reconstruct_from_event(self, event, payment):
        # naive implementation
        event_types = {
            'PaymentCreated': PaymentCreated,
            'PaymentAuthorized': PaymentAuthorized,
            'PaymentSettled': PaymentSettled,
            'PaymentRefunded': PaymentRefunded,
            'PaymentDeclined': PaymentDeclined
        }

        converted = event.json()
        domain_event = event_types[event.type](**converted)
        payment.reconstruct_from_event(domain_event)

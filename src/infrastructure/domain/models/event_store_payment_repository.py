import asyncio
import photonpump

from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId
from src.domain.models.payment_repository import PaymentRepository


class EventStorePaymentRepository(PaymentRepository):
    def __init__(self, username: str, password: str):
        self._loop = asyncio.get_event_loop()
        self._client = photonpump.connect(loop=self._loop, username=username, password=password)
        self._connected = False

    async def save(self, payment: Payment) -> bool:
        await self.check_connection()

        stream_name = self._create_stream_name(payment.payment_id)
        for event in payment.events:
            # We could publish in batches
            await self._client.publish_event(stream_name, event.type, event.encode())

        return True

    async def check_connection(self):
        if not self._connected:
            await self._client.connect()
            self._connected = True

    def _create_stream_name(self, payment_id: PaymentId) -> str:
        return f'payment-{payment_id.value}'

    async def find_by_id(self, payment_id: PaymentId) -> Payment:
        await self.check_connection()

        stream_name = self._create_stream_name(payment_id)
        # subscription = await self._client.subscribe_to(stream=stream_name, start_from=0)
        # async for event in subscription.events:
        #     print(event.json())
        #     print(event.event_number)
        async for event in self._client.stream(stream_name):
            print(event)

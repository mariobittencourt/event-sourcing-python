import asyncio
import photonpump

from src.domain.models.payment import Payment
from src.domain.models.payment_repository import PaymentRepository


class EventStorePaymentRepository(PaymentRepository):
    def __init__(self, username: str, password: str):
        self._loop = asyncio.get_event_loop()
        self._client = client = photonpump.connect(loop=self._loop, username='admin', password='changeit')
        self._connected = False

    async def save(self, payment: Payment) -> bool:
        if not self._connected:
            await self._client.connect()
            self._connected = True

        for event in payment.events:
            result = await self._client.publish_event(f'payment-{payment.payment_id.value}', event.type, event.encode())
            print(result)

from photonpump.connection import Client
from photonpump.conversations import VolatileSubscription

from src.domain.services.payment_stream_service import PaymentStreamService
from src.domain.views.payment_projectionist import PaymentProjectionist
from src.infrastructure.domain.models.event_store_payment_repository import EventStorePaymentRepository


class EventStoreStreamService(PaymentStreamService):
    def __init__(self, client: Client):
        self.client = client

    async def subscribe(self, stream: str, start_from: int, projectionist: PaymentProjectionist):
        await self.client.connect()
        subscription: VolatileSubscription = await self.client.subscribe_to(stream=stream, start_from=start_from)
        async for event in subscription.events:
            projectionist.handle(await EventStorePaymentRepository.convert_to_domain_event(event))
from src.domain.models.domain_event import DomainEvent
from src.domain.services.payment_stream_service import PaymentStreamService
from src.domain.views.payment_projector import PaymentProjector


class PaymentProjectionist:
    def __init__(self, projector: PaymentProjector, stream_service: PaymentStreamService):
        self.projector = projector
        self.stream_service = stream_service

    async def start(self):
        # load the ledger last position
        # subscribe to the stream from the ledger position
        await self.stream_service.subscribe(stream='$ce-payments', start_from=0, projectionist=self)

    def handle(self, event: DomainEvent):
        # pass it to the projector
        self.projector.apply(event)
        # if all goes well, acknowledge the ledger to know when to resume next time.



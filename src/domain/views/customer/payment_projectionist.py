from src.domain.models.domain_event import DomainEvent
from src.domain.services.payment_stream_service import PaymentStreamService
from src.domain.views.ledger_repository import LedgerRepository
from src.domain.views.customer.payment_projector import PaymentProjector


class PaymentProjectionist:
    def __init__(self, projector: PaymentProjector, stream_service: PaymentStreamService, ledger_repository: LedgerRepository, ledger_name: str):
        self.projector = projector
        self.stream_service = stream_service
        self.ledger_repository = ledger_repository
        self.ledger = None
        self.ledger_name = ledger_name

    async def start(self):
        # load the ledger last position
        self.ledger = self.ledger_repository.find_by_projection_name(self.ledger_name)

        # subscribe to the stream from the ledger position
        if self.ledger.last_position == -1:
            self.ledger.last_position = 0
        else:
            self.ledger.last_position += 1

        await self.stream_service.subscribe(stream='$ce-payments', start_from=self.ledger.last_position, projectionist=self)

    def handle(self, event: DomainEvent):
        # pass it to the projector
        self.projector.apply(event)
        # if all goes well, acknowledge the ledger to know when to resume next time
        # in practice, you can decide to batch the updates and for sure you would have to handle temporary issues to retry
        self.ledger_repository.update(self.ledger)
        self.ledger.last_position += 1




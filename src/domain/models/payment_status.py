from enum import Enum


class PaymentStatus(Enum):
    PENDING_PROCESSING = 'PENDING_PROCESSING'
    SETTLED = 'SETTLED'
    AUTHORIZED = 'AUTHORIZED'
    REFUNDED = 'REFUNDED'

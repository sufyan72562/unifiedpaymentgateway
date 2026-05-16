from enum import Enum


class PaymentProvider(str, Enum):
    PROVIDER_A = "provider_a"
    PROVIDER_B = "provider_b"


class PaymentStatus(str, Enum):
    PROCESSING = "PROCESSING"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
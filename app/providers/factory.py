from app.core.enums import PaymentProvider

from app.providers.provider_a import ProviderA
from app.providers.provider_b import ProviderB

PROVIDERS = {
    PaymentProvider.PROVIDER_A: ProviderA,
    PaymentProvider.PROVIDER_B: ProviderB,
}


def get_provider(provider: PaymentProvider):

    provider_class = PROVIDERS.get(provider)

    if not provider_class:
        raise ValueError("Unsupported payment provider")

    return provider_class()
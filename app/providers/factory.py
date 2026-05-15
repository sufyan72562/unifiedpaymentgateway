from app.core.enums import PaymentProvider

from app.providers.provider_a import ProviderA
from app.providers.provider_b import ProviderB


def get_provider(provider: PaymentProvider):

    if provider == PaymentProvider.PROVIDER_A:
        return ProviderA()

    if provider == PaymentProvider.PROVIDER_B:
        return ProviderB()

    raise ValueError("Unsupported payment provider")
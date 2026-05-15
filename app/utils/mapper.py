from app.core.enums import PaymentStatus


def normalize_provider_response(
    provider: str,
    response: dict,
):
    if provider == "provider_a":
        return {
            "provider_reference": response["id"],
            "amount": float(response["amount"]),
            "currency": response["currency"],
            "status": PaymentStatus.PENDING.value,
            "raw_response": response,
        }

    if provider == "provider_b":
        return {
            "provider_reference": response["transactionId"],
            "amount": float(response["totalAmount"]),
            "currency": response["currencyCode"],
            "status": PaymentStatus.PENDING.value,
            "raw_response": response,
        }

    raise ValueError("Unsupported provider")
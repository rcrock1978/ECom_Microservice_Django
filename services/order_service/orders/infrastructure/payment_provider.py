class PaymentProvider:
    def create_payment_session(self, order_number: str, amount: float) -> dict[str, str]:
        return {
            "payment_url": f"https://payments.example.com/checkout/{order_number}",
            "session_id": f"sess-{order_number}",
            "amount": f"{amount:.2f}",
        }

    def is_success(self, provider_status: str) -> bool:
        return provider_status.lower() == "success"

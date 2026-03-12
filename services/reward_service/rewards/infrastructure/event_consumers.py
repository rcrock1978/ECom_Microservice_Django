class RewardEventConsumer:
    def __init__(self) -> None:
        self.transactions: list[dict[str, object]] = []

    def handle_order_confirmed(self, payload: dict[str, object]) -> None:
        total = float(payload.get("total_amount", 0))
        points = int(total // 10)
        self.transactions.append(
            {
                "user_id": payload.get("user_id"),
                "order_number": payload.get("order_number"),
                "points": points,
                "type": "credit",
            }
        )

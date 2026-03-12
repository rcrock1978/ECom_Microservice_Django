class ValidateRedemptionUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, points: int) -> dict[str, object]:
        account = self.repository.get_by_user_id(user_id)
        available = account.available_points if account else 0
        is_valid = bool(account and account.can_redeem(points))
        return {"is_valid": is_valid, "available_points": available}

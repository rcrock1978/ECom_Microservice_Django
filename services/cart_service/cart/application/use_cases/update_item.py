class UpdateItemUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, item_id: str, quantity: int):
        cart = self.repository.get_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")
        cart.update_item(item_id, quantity)
        return self.repository.save(cart)

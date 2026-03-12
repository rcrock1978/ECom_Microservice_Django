class RemoveItemUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, item_id: str):
        cart = self.repository.get_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")
        cart.remove_item(item_id)
        return self.repository.save(cart)

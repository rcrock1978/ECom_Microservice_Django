from cart.domain.entities import Cart


class AddItemUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, product_id: str, product_name: str, product_price: float, quantity: int) -> Cart:
        cart = self.repository.get_by_user_id(user_id) or Cart.create(user_id=user_id)
        cart.add_item(product_id=product_id, product_name=product_name, product_price=product_price, quantity=quantity)
        return self.repository.save(cart)

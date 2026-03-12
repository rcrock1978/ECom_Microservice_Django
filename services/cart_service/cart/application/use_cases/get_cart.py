from cart.domain.entities import Cart


class GetCartUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str) -> Cart:
        cart = self.repository.get_by_user_id(user_id)
        if not cart:
            cart = Cart.create(user_id=user_id)
            self.repository.save(cart)
        return cart

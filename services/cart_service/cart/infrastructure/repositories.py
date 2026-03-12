from cart.domain.entities import Cart


class InMemoryCartRepository:
    def __init__(self) -> None:
        self.carts: dict[str, Cart] = {}

    def get_by_user_id(self, user_id: str) -> Cart | None:
        return self.carts.get(user_id)

    def save(self, cart: Cart) -> Cart:
        self.carts[cart.user_id] = cart
        return cart

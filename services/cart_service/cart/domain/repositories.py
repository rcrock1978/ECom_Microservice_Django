from abc import ABC, abstractmethod

from cart.domain.entities import Cart


class CartRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Cart | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        raise NotImplementedError

from cart.application.use_cases.add_item import AddItemUseCase
from cart.application.use_cases.apply_coupon import ApplyCouponUseCase
from cart.application.use_cases.get_cart import GetCartUseCase
from cart.application.use_cases.remove_coupon import RemoveCouponUseCase
from cart.application.use_cases.remove_item import RemoveItemUseCase
from cart.application.use_cases.update_item import UpdateItemUseCase
from cart.infrastructure.repositories import InMemoryCartRepository
from cart.presentation.serializers import serialize_cart


class CartFacade:
    def __init__(self, repository: InMemoryCartRepository) -> None:
        self.repository = repository
        self.get_cart_uc = GetCartUseCase(repository)
        self.add_item_uc = AddItemUseCase(repository)
        self.update_item_uc = UpdateItemUseCase(repository)
        self.remove_item_uc = RemoveItemUseCase(repository)
        self.apply_coupon_uc = ApplyCouponUseCase(repository)
        self.remove_coupon_uc = RemoveCouponUseCase(repository)

    @classmethod
    def in_memory(cls) -> "CartFacade":
        return cls(InMemoryCartRepository())

    def get_cart(self, user_id: str) -> dict[str, object]:
        cart = self.get_cart_uc.execute(user_id)
        return {"status": 200, "data": serialize_cart(cart)}

    def add_item(self, user_id: str, product_id: str, product_name: str, product_price: float, quantity: int) -> dict[str, object]:
        cart = self.add_item_uc.execute(user_id, product_id, product_name, product_price, quantity)
        return {"status": 200, "data": serialize_cart(cart)}

    def update_item(self, user_id: str, item_id: str, quantity: int) -> dict[str, object]:
        cart = self.update_item_uc.execute(user_id, item_id, quantity)
        return {"status": 200, "data": serialize_cart(cart)}

    def remove_item(self, user_id: str, item_id: str) -> dict[str, object]:
        cart = self.remove_item_uc.execute(user_id, item_id)
        return {"status": 200, "data": serialize_cart(cart)}

    def apply_coupon(self, user_id: str, coupon_code: str) -> dict[str, object]:
        cart = self.apply_coupon_uc.execute(user_id, coupon_code)
        return {"status": 200, "data": serialize_cart(cart)}

    def remove_coupon(self, user_id: str) -> dict[str, object]:
        cart = self.remove_coupon_uc.execute(user_id)
        return {"status": 200, "data": serialize_cart(cart)}

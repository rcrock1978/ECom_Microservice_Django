from cart.application.use_cases.add_item import AddItemUseCase
from cart.application.use_cases.apply_coupon import ApplyCouponUseCase
from cart.domain.entities import Cart
from cart.infrastructure.repositories import InMemoryCartRepository


def test_add_item_use_case_creates_cart_and_item() -> None:
    repository = InMemoryCartRepository()
    use_case = AddItemUseCase(repository)

    result = use_case.execute(user_id="user-1", product_id="p1", product_name="Headphones", product_price=79.99, quantity=1)

    assert result.user_id == "user-1"
    assert result.item_count == 1


def test_apply_coupon_sets_coupon_code() -> None:
    repository = InMemoryCartRepository()
    cart = Cart.create(user_id="user-1")
    repository.save(cart)
    use_case = ApplyCouponUseCase(repository)

    result = use_case.execute(user_id="user-1", coupon_code="SAVE20")

    assert result.coupon_code == "SAVE20"

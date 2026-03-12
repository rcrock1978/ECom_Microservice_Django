from coupons.domain.entities import Coupon


def test_coupon_percentage_discount_with_cap() -> None:
    coupon = Coupon.create(
        code="SAVE20",
        discount_type="percentage",
        discount_value=20,
        min_order_amount=50,
        max_discount_amount=30,
    )

    discount = coupon.calculate_discount(200)

    assert discount == 30


def test_coupon_fixed_discount_respects_minimum_order() -> None:
    coupon = Coupon.create(
        code="FLAT10",
        discount_type="fixed",
        discount_value=10,
        min_order_amount=100,
    )

    assert coupon.calculate_discount(99) == 0
    assert coupon.calculate_discount(120) == 10

from coupons.domain.entities import Coupon


def test_coupon_cannot_redeem_after_usage_limit() -> None:
    coupon = Coupon.create(
        code="LIMIT2",
        discount_type="fixed",
        discount_value=15,
        usage_limit=2,
    )

    assert coupon.can_redeem() is True
    coupon.mark_redeemed()
    assert coupon.can_redeem() is True
    coupon.mark_redeemed()
    assert coupon.can_redeem() is False


def test_coupon_deactivated_cannot_be_redeemed() -> None:
    coupon = Coupon.create(code="OFF", discount_type="fixed", discount_value=5)

    coupon.is_active = False

    assert coupon.can_redeem() is False

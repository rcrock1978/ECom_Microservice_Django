from coupons.presentation.views import CouponFacade


def test_validate_and_redeem_coupon_flow() -> None:
    facade = CouponFacade.in_memory_seeded()

    validated = facade.validate_coupon("SAVE10", subtotal=120)
    assert validated["status"] == 200
    assert validated["data"]["is_valid"] is True
    assert validated["data"]["discount_amount"] == "10.00"

    redeemed = facade.redeem_coupon("SAVE10", user_id="user-1")
    assert redeemed["status"] == 200
    assert redeemed["data"]["code"] == "SAVE10"


def test_admin_coupon_crud_flow() -> None:
    facade = CouponFacade.in_memory_seeded()

    created = facade.create_coupon(
        code="FLASH15",
        discount_type="percentage",
        discount_value=15,
        min_order_amount=50,
        usage_limit=10,
    )
    assert created["status"] == 201

    updated = facade.update_coupon("FLASH15", discount_value=12, is_active=True)
    assert updated["status"] == 200
    assert updated["data"]["discount_value"] == "12.00"

    listed = facade.list_coupons(active_only=True)
    assert listed["status"] == 200
    assert any(item["code"] == "FLASH15" for item in listed["data"])

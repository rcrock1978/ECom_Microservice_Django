from coupons.application.use_cases.create_coupon import CreateCouponUseCase
from coupons.application.use_cases.list_coupons import ListCouponsUseCase
from coupons.application.use_cases.redeem_coupon import RedeemCouponUseCase
from coupons.application.use_cases.update_coupon import UpdateCouponUseCase
from coupons.application.use_cases.validate_coupon import ValidateCouponUseCase
from coupons.domain.entities import Coupon
from coupons.infrastructure.repositories import InMemoryCouponRepository
from coupons.presentation.serializers import serialize_coupon


class CouponFacade:
    def __init__(self, repository: InMemoryCouponRepository) -> None:
        self.repository = repository
        self.validate_uc = ValidateCouponUseCase(repository)
        self.redeem_uc = RedeemCouponUseCase(repository)
        self.create_uc = CreateCouponUseCase(repository)
        self.update_uc = UpdateCouponUseCase(repository)
        self.list_uc = ListCouponsUseCase(repository)

    @classmethod
    def in_memory_seeded(cls) -> "CouponFacade":
        repository = InMemoryCouponRepository()
        repository.save(
            Coupon.create(
                code="SAVE10",
                discount_type="fixed",
                discount_value=10,
                min_order_amount=100,
                usage_limit=100,
            )
        )
        return cls(repository)

    def validate_coupon(self, code: str, subtotal: float) -> dict[str, object]:
        result = self.validate_uc.execute(code=code, subtotal=subtotal)
        return {
            "status": 200,
            "data": {
                "is_valid": result["is_valid"],
                "discount_amount": f"{float(result['discount_amount']):.2f}",
            },
        }

    def redeem_coupon(self, code: str, user_id: str) -> dict[str, object]:
        coupon = self.redeem_uc.execute(code=code, user_id=user_id)
        return {"status": 200, "data": serialize_coupon(coupon)}

    def create_coupon(
        self,
        code: str,
        discount_type: str,
        discount_value: float,
        min_order_amount: float = 0,
        max_discount_amount: float | None = None,
        usage_limit: int | None = None,
    ) -> dict[str, object]:
        coupon = self.create_uc.execute(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            min_order_amount=min_order_amount,
            max_discount_amount=max_discount_amount,
            usage_limit=usage_limit,
        )
        return {"status": 201, "data": serialize_coupon(coupon)}

    def update_coupon(self, code: str, **fields) -> dict[str, object]:
        coupon = self.update_uc.execute(code, **fields)
        return {"status": 200, "data": serialize_coupon(coupon)}

    def list_coupons(self, active_only: bool = False) -> dict[str, object]:
        coupons = self.list_uc.execute(active_only=active_only)
        return {"status": 200, "data": [serialize_coupon(item) for item in coupons]}

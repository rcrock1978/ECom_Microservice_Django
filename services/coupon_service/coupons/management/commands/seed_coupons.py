from django.core.management.base import BaseCommand

from coupon_service.models import CouponModel


class Command(BaseCommand):
    help = "Seed sample coupons"

    def handle(self, *args, **options):
        sample_coupons = [
            {
                "id": "coupon-save10",
                "code": "SAVE10",
                "discount_type": "fixed",
                "discount_value": "10.00",
                "min_order_amount": "50.00",
                "max_discount_amount": None,
                "usage_limit": 100,
                "used_count": 0,
                "is_active": True,
            },
            {
                "id": "coupon-welcome15",
                "code": "WELCOME15",
                "discount_type": "percentage",
                "discount_value": "15.00",
                "min_order_amount": "75.00",
                "max_discount_amount": "40.00",
                "usage_limit": 200,
                "used_count": 0,
                "is_active": True,
            },
        ]

        created_count = 0
        for payload in sample_coupons:
            _, created = CouponModel.objects.get_or_create(code=payload["code"], defaults=payload)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created_count} coupon(s)."))

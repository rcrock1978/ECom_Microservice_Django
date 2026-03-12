from uuid import uuid4

from django.core.management.base import BaseCommand

from catalog.models import CategoryModel, ProductModel


class Command(BaseCommand):
    help = "Seed sample products and categories"

    def handle(self, *args, **options):
        electronics, _ = CategoryModel.objects.get_or_create(
            slug="electronics",
            defaults={
                "id": str(uuid4()),
                "name": "Electronics",
                "description": "Electronic products",
                "is_active": True,
            },
        )

        samples = [
            {
                "name": "Wireless Headphones",
                "slug": "wireless-headphones",
                "description": "Noise cancelling bluetooth headphones",
                "price": 79.99,
                "stock_quantity": 25,
                "image_url": "https://example.com/headphones.jpg",
            },
            {
                "name": "Portable Speaker",
                "slug": "portable-speaker",
                "description": "Compact speaker",
                "price": 39.99,
                "stock_quantity": 10,
                "image_url": "https://example.com/speaker.jpg",
            },
        ]

        created = 0
        for item in samples:
            _, was_created = ProductModel.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "id": str(uuid4()),
                    "category_id": electronics.id,
                    "is_active": True,
                    **item,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} product(s)."))

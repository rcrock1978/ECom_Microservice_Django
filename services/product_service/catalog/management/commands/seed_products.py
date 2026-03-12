from django.core.management.base import BaseCommand

from services.product_service.catalog.infrastructure.models import Category, Product


class Command(BaseCommand):
    help = "Seed sample categories and products for development"

    def handle(self, *args, **options):
        # clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # create categories
        cats = []
        for i in range(1, 6):
            cat = Category.objects.create(name=f"Category {i}")
            cats.append(cat)
        # create some child categories for first category
        sub = Category.objects.create(name="Subcategory 1", parent=cats[0])
        cats.append(sub)

        # create products
        for i in range(1, 11):
            Product.objects.create(
                name=f"Product {i}",
                slug=f"product-{i}",
                description=f"Description for product {i}",
                price=i * 1.99,
                category=cats[i % len(cats)] if cats else None,
            )

        self.stdout.write(self.style.SUCCESS("Seeded categories and products"))

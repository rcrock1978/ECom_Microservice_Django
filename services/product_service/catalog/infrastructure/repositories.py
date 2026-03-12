from __future__ import annotations
from typing import Optional, List

from django.db.models import QuerySet, Q

from services.product_service.catalog.infrastructure.models import Product, Category


class ProductRepository:
    def list(self, keyword: Optional[str] = None, category_id: Optional[int] = None) -> QuerySet[Product]:
        qs = Product.objects.all()
        if keyword:
            qs = qs.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            )
        if category_id is not None:
            qs = qs.filter(category_id=category_id)
        return qs

    def get_by_slug(self, slug: str) -> Optional[Product]:
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None


class CategoryRepository:
    def list_roots(self) -> QuerySet[Category]:
        return Category.objects.filter(parent__isnull=True).prefetch_related('children')

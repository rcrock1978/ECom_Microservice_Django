from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Category:
    id: str
    name: str
    slug: str
    description: str | None = None
    parent_id: str | None = None
    is_active: bool = True

    @classmethod
    def create(cls, name: str, slug: str, description: str | None = None, parent_id: str | None = None) -> "Category":
        return cls(id=str(uuid4()), name=name, slug=slug, description=description, parent_id=parent_id)


@dataclass
class Product:
    id: str
    name: str
    slug: str
    description: str
    price: float
    category_id: str
    stock_quantity: int
    image_url: str | None = None
    is_active: bool = True

    @property
    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0 and self.is_active

    @classmethod
    def create(
        cls,
        name: str,
        slug: str,
        description: str,
        price: float,
        category_id: str,
        stock_quantity: int,
        image_url: str | None = None,
    ) -> "Product":
        return cls(
            id=str(uuid4()),
            name=name,
            slug=slug,
            description=description,
            price=price,
            category_id=category_id,
            stock_quantity=stock_quantity,
            image_url=image_url,
        )

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class CartItem:
    id: str
    product_id: str
    product_name: str
    product_price: float
    quantity: int

    @property
    def line_total(self) -> float:
        return self.product_price * self.quantity


@dataclass
class Cart:
    id: str
    user_id: str
    items: list[CartItem] = field(default_factory=list)
    coupon_code: str | None = None

    @classmethod
    def create(cls, user_id: str) -> "Cart":
        return cls(id=str(uuid4()), user_id=user_id)

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def subtotal(self) -> float:
        return sum(item.line_total for item in self.items)

    def add_item(self, product_id: str, product_name: str, product_price: float, quantity: int) -> CartItem:
        existing = next((item for item in self.items if item.product_id == product_id), None)
        if existing:
            existing.quantity += quantity
            return existing
        item = CartItem(
            id=str(uuid4()),
            product_id=product_id,
            product_name=product_name,
            product_price=product_price,
            quantity=quantity,
        )
        self.items.append(item)
        return item

    def update_item(self, item_id: str, quantity: int) -> None:
        for item in self.items:
            if item.id == item_id:
                item.quantity = quantity
                return
        raise ValueError("Item not found")

    def remove_item(self, item_id: str) -> None:
        self.items = [item for item in self.items if item.id != item_id]

    def apply_coupon(self, coupon_code: str) -> None:
        self.coupon_code = coupon_code

    def remove_coupon(self) -> None:
        self.coupon_code = None

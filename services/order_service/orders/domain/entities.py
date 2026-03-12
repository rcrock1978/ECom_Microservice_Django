from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class OrderItem:
    id: str
    product_id: str
    product_name: str
    unit_price: float
    quantity: int

    @property
    def line_total(self) -> float:
        return self.unit_price * self.quantity

    @classmethod
    def create(cls, product_id: str, product_name: str, unit_price: float, quantity: int) -> "OrderItem":
        return cls(
            id=str(uuid4()),
            product_id=product_id,
            product_name=product_name,
            unit_price=unit_price,
            quantity=quantity,
        )


@dataclass
class Order:
    id: str
    order_number: str
    user_id: str
    items: list[OrderItem]
    status: str = "pending"
    discount_amount: float = 0.0
    email: str | None = None

    @classmethod
    def create(cls, user_id: str, items: list[OrderItem], discount_amount: float = 0.0, email: str | None = None) -> "Order":
        order_id = str(uuid4())
        return cls(
            id=order_id,
            order_number=f"ORD-{order_id[:8].upper()}",
            user_id=user_id,
            items=items,
            discount_amount=discount_amount,
            email=email,
        )

    @property
    def subtotal(self) -> float:
        return sum(item.line_total for item in self.items)

    @property
    def total_amount(self) -> float:
        return max(self.subtotal - self.discount_amount, 0.0)

    def mark_paid(self) -> None:
        if self.status != "pending":
            raise ValueError("Only pending orders can be marked paid")
        self.status = "paid"

    def mark_shipped(self) -> None:
        if self.status != "paid":
            raise ValueError("Order must be paid before shipping")
        self.status = "shipped"

    def cancel(self) -> None:
        self.status = "cancelled"

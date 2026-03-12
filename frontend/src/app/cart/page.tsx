"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import { CartDrawer } from "@/components/cart/CartDrawer";
import { useCart } from "@/lib/cart/context";

type CartData = {
  items: Array<{ id: string; product_name: string; quantity: number; line_total: string }>;
  item_count: number;
  subtotal: string;
};

export default function CartPage() {
  const [cart, setCart] = useState<CartData>({ items: [], item_count: 0, subtotal: "0.00" });
  const { setItemCount } = useCart();

  useEffect(() => {
    apiRequest<{ data: CartData }>("/api/v1/cart/")
      .then((result) => {
        setCart(result.data);
        setItemCount(result.data.item_count);
      })
      .catch(() => {
        setCart({ items: [], item_count: 0, subtotal: "0.00" });
        setItemCount(0);
      });
  }, [setItemCount]);

  const handleRemove = async (itemId: string) => {
    const result = await apiRequest<{ data: CartData }>(`/api/v1/cart/items/${itemId}/`, { method: "DELETE" });
    setCart(result.data);
    setItemCount(result.data.item_count);
  };

  return (
    <div>
      <h2>Cart</h2>
      <p>Subtotal: {cart.subtotal}</p>
      <CartDrawer cart={cart} onRemove={handleRemove} />
    </div>
  );
}

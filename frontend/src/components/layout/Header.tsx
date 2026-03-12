"use client";

import { useCart } from "@/lib/cart/context";

export function Header() {
  const { itemCount } = useCart();
  return (
    <header>
      <h1>Mango Store</h1>
      <p>Cart: {itemCount}</p>
    </header>
  );
}

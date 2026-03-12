"use client";

import { createContext, useContext, useMemo, useState } from "react";

type CartContextValue = {
  itemCount: number;
  setItemCount: (value: number) => void;
  addToCart: (productId: string, productName: string, productPrice: number, quantity?: number) => Promise<void>;
};

const CartContext = createContext<CartContextValue | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [itemCount, setItemCount] = useState(0);
  async function addToCart(productId: string, productName: string, productPrice: number, quantity: number = 1): Promise<void> {
    const { apiRequest } = await import("@/lib/api/client");
    const result = await apiRequest<{ data: { item_count: number } }>("/api/v1/cart/items/", {
      method: "POST",
      body: JSON.stringify({ product_id: productId, product_name: productName, product_price: productPrice, quantity }),
    });
    setItemCount(result.data.item_count);
  }

  const value = useMemo(() => ({ itemCount, setItemCount, addToCart }), [itemCount]);
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used inside CartProvider");
  }
  return context;
}

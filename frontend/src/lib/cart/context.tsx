"use client";

import { createContext, useContext, useMemo, useState } from "react";

type CartContextValue = {
  itemCount: number;
  setItemCount: (value: number) => void;
};

const CartContext = createContext<CartContextValue | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [itemCount, setItemCount] = useState(0);
  const value = useMemo(() => ({ itemCount, setItemCount }), [itemCount]);
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used inside CartProvider");
  }
  return context;
}

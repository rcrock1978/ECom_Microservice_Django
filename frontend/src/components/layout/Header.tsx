"use client";

import { useAuth } from "@/lib/auth/context";
import { useCart } from "@/lib/cart/context";

export function Header() {
  const { itemCount } = useCart();
  const { isAuthenticated, userEmail, logout } = useAuth();
  return (
    <header>
      <h1>Mango Store</h1>
      <p>Cart: {itemCount}</p>
      {isAuthenticated ? (
        <div>
          <span>{userEmail}</span>
          <button type="button" onClick={() => void logout()}>
            Logout
          </button>
        </div>
      ) : (
        <span>Guest</span>
      )}
    </header>
  );
}

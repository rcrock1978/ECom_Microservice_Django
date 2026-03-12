"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createOrder, getCheckoutResultRoute } from "@/lib/api";

export default function CheckoutPage() {
  const router = useRouter();
  const [status, setStatus] = useState<string>("");

  async function handleCheckout() {
    try {
      const payload = await createOrder([{ product_id: "p1", product_name: "Headphones", unit_price: 99, quantity: 1 }]);
      setStatus(`Order created: ${payload.data.order_number}`);
      router.push(getCheckoutResultRoute(true));
    } catch {
      setStatus("Checkout failed");
      router.push(getCheckoutResultRoute(false));
    }
  }

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-semibold">Checkout</h1>
      <button className="mt-4 rounded bg-black px-4 py-2 text-white" onClick={handleCheckout}>
        Place Order
      </button>
      {status ? <p className="mt-4">{status}</p> : null}
    </main>
  );
}

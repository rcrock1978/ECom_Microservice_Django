"use client";

import { useEffect } from "react";
import { trackFirstPurchaseSuccess } from "@/lib/analytics/funnel";

export default function CheckoutSuccessPage() {
  useEffect(() => {
    trackFirstPurchaseSuccess({ orderNumber: "ORD-SUCCESS", source: "checkout-success-page" });
  }, []);

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-semibold">Payment Successful</h1>
      <p className="mt-2">Your order has been confirmed.</p>
    </main>
  );
}

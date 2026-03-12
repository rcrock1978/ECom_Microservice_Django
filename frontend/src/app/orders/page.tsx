"use client";

import { useEffect, useState } from "react";
import { fetchOrders } from "@/lib/api";

type OrderSummary = {
  order_number: string;
  status: string;
  total_amount: string;
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<OrderSummary[]>([]);

  useEffect(() => {
    fetchOrders()
      .then((response) => setOrders(response.data))
      .catch(() => setOrders([]));
  }, []);

  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="text-2xl font-semibold">My Orders</h1>
      <ul className="mt-4 space-y-2">
        {orders.map((order) => (
          <li key={order.order_number} className="rounded border p-3">
            <div>{order.order_number}</div>
            <div className="text-sm text-gray-600">{order.status}</div>
            <div className="text-sm">${order.total_amount}</div>
          </li>
        ))}
      </ul>
    </main>
  );
}

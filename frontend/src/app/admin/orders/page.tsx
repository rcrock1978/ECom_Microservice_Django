"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { fetchOrders } from "@/lib/api/client";

type Order = { order_number: string; status: string; total_amount: string };

export default function AdminOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetchOrders()
      .then((response) => setOrders(response.data))
      .catch(() => setOrders([]));
  }, []);

  return (
    <section>
      <h2 className="text-xl font-semibold">Orders</h2>
      <ul className="mt-3 space-y-2">
        {orders.map((order) => (
          <li key={order.order_number} className="rounded border p-3">
            <Link href={`/admin/orders/${order.order_number}`}>
              {order.order_number} — {order.status}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

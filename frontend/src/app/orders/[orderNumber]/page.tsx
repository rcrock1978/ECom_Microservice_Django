"use client";

import { useEffect, useState } from "react";
import { fetchOrder } from "@/lib/api";

type OrderDetail = {
  order_number: string;
  status: string;
  total_amount: string;
};

export default function OrderDetailPage({ params }: { params: { orderNumber: string } }) {
  const [order, setOrder] = useState<OrderDetail | null>(null);

  useEffect(() => {
    fetchOrder(params.orderNumber)
      .then((response) => setOrder(response.data))
      .catch(() => setOrder(null));
  }, [params.orderNumber]);

  if (!order) {
    return <main className="mx-auto max-w-3xl p-6">Order not found.</main>;
  }

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-semibold">Order {order.order_number}</h1>
      <p className="mt-2">Status: {order.status}</p>
      <p>Total: ${order.total_amount}</p>
    </main>
  );
}

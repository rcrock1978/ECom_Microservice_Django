"use client";

import { useState } from "react";
import { apiRequest } from "@/lib/api";

export default function AdminOrderDetailPage({ params }: { params: { orderNumber: string } }) {
  const [status, setStatus] = useState("");

  async function markShipped() {
    try {
      await apiRequest(`/api/v1/orders/admin/${params.orderNumber}/status/`, {
        method: "PATCH",
        body: JSON.stringify({ status: "shipped" }),
      });
      setStatus("Order updated");
    } catch {
      setStatus("Update failed");
    }
  }

  return (
    <section>
      <h2 className="text-xl font-semibold">Order {params.orderNumber}</h2>
      <button className="mt-3 rounded border px-3 py-1" onClick={markShipped}>Mark Shipped</button>
      {status ? <p className="mt-3">{status}</p> : null}
    </section>
  );
}

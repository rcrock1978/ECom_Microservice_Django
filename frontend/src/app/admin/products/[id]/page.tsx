"use client";

import { useState } from "react";
import { apiRequest } from "@/lib/api";

export default function AdminProductDetailPage({ params }: { params: { id: string } }) {
  const [status, setStatus] = useState("");

  async function updateProduct() {
    try {
      await apiRequest(`/api/v1/admin/catalog/products/${params.id}/`, {
        method: "PATCH",
        body: JSON.stringify({ price: 24.99 }),
      });
      setStatus("Product updated");
    } catch {
      setStatus("Update failed");
    }
  }

  return (
    <section>
      <h2 className="text-xl font-semibold">Product {params.id}</h2>
      <button className="mt-3 rounded border px-3 py-1" onClick={updateProduct}>Update Price</button>
      {status ? <p className="mt-3">{status}</p> : null}
    </section>
  );
}

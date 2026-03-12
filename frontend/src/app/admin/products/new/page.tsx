"use client";

import { useState } from "react";
import { apiRequest } from "@/lib/api";

export default function AdminNewProductPage() {
  const [status, setStatus] = useState("");

  async function createProduct() {
    try {
      await apiRequest("/api/v1/admin/catalog/products/", {
        method: "POST",
        body: JSON.stringify({
          name: "New Product",
          slug: "new-product",
          description: "Created from admin",
          price: 19.99,
          category_slug: "electronics",
          stock_quantity: 10,
        }),
      });
      setStatus("Product created");
    } catch {
      setStatus("Create failed");
    }
  }

  return (
    <section>
      <h2 className="text-xl font-semibold">Create Product</h2>
      <button className="mt-3 rounded border px-3 py-1" onClick={createProduct}>Create</button>
      {status ? <p className="mt-3">{status}</p> : null}
    </section>
  );
}

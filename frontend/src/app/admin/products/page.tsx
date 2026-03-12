"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";

type Product = { id: string; name: string; slug: string; price: string };

export default function AdminProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    apiRequest<{ data: Product[] }>("/api/v1/products/")
      .then((response) => setProducts(response.data))
      .catch(() => setProducts([]));
  }, []);

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Products</h2>
        <Link href="/admin/products/new" className="rounded border px-3 py-1">New Product</Link>
      </div>
      <ul className="space-y-2">
        {products.map((product) => (
          <li key={product.id} className="rounded border p-3">
            <Link href={`/admin/products/${product.id}`}>
              {product.name} — ${product.price}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

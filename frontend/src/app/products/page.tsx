"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import { ProductFilters } from "@/components/products/ProductFilters";
import { ProductGrid } from "@/components/products/ProductGrid";

type Product = {
  name: string;
  slug: string;
  price: string;
  is_in_stock: boolean;
};

export default function ProductsPage() {
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    const endpoint = query.trim().length > 0 ? `/api/v1/products/?search=${encodeURIComponent(query)}` : "/api/v1/products/";
    apiRequest<{ data: Product[] }>(endpoint)
      .then((result) => setProducts(result.data ?? []))
      .catch(() => setProducts([]));
  }, [query]);

  return (
    <div>
      <h2>Products</h2>
      <ProductFilters query={query} onQueryChange={setQuery} />
      <ProductGrid products={products} />
    </div>
  );
}

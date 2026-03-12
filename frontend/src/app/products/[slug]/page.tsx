"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";

type ProductDetail = {
  name: string;
  slug: string;
  description: string;
  price: string;
  stock_quantity: number;
};

export default function ProductDetailPage({ params }: { params: { slug: string } }) {
  const [product, setProduct] = useState<ProductDetail | null>(null);

  useEffect(() => {
    apiRequest<{ data: ProductDetail }>(`/api/v1/products/${params.slug}/`)
      .then((result) => setProduct(result.data))
      .catch(() => setProduct(null));
  }, [params.slug]);

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p>{product.price}</p>
      <p>Stock: {product.stock_quantity}</p>
    </div>
  );
}

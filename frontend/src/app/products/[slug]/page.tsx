import React from 'react';
import { fetcher } from '../../../lib/api/client';

type Product = {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: number;
};

export default async function ProductDetailPage({ params }: { params: { slug: string } }) {
  let product: Product | null = null;
  try {
    product = await fetcher<Product>(`/api/products/${params.slug}`);
  } catch (e) {
    console.error('error fetching product', e);
  }
  if (!product) {
    return <p>Product not found</p>;
  }
  return (
    <main>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>${product.price.toFixed(2)}</p>
    </main>
  );
}

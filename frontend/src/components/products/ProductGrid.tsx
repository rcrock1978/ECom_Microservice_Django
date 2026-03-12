import React from 'react';
import { ProductCard } from './ProductCard';

type Product = {
  id: number;
  name: string;
  slug: string;
  price: number;
};

interface Props {
  products: Product[];
}

export const ProductGrid: React.FC<Props> = ({ products }) => {
  return (
    <div className="product-grid">
      {products.map((p) => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  );
};

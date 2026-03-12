import React from 'react';

type Product = {
  id: number;
  name: string;
  slug: string;
  price: number;
};

interface Props {
  product: Product;
}

export const ProductCard: React.FC<Props> = ({ product }) => {
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>${product.price.toFixed(2)}</p>
      <a href={`/products/${product.slug}`}>View details</a>
    </div>
  );
};

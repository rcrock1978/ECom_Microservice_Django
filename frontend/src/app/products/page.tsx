import React from 'react';
import { fetcher } from '../../lib/api/client';
import { ProductGrid } from '../../components/products/ProductGrid';

type Product = {
  id: number;
  name: string;
  slug: string;
  price: number;
};

export default async function ProductsPage() {
  let products: Product[] = [];
  try {
    products = await fetcher<Product[]>('/api/products');
  } catch (e) {
    console.error('failed to load products', e);
  }

  return (
    <main>
      <h1>Products</h1>
      <div className="catalog-layout">
        <aside className="sidebar">
          {/* TODO: category sidebar */}
          <p>Categories</p>
        </aside>
        <section className="product-list">
          <div className="search-bar">
            {/* TODO: search input */}
            <input type="text" placeholder="Search..." />
          </div>
          <ProductGrid products={products} />
          <div className="pagination">
            {/* TODO: pagination controls */}
            <button disabled>Prev</button>
            <button>Next</button>
          </div>
        </section>
      </div>
    </main>
  );
}

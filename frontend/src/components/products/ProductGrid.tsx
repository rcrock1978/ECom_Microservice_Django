import { ProductCard } from "./ProductCard";

type Product = {
  name: string;
  slug: string;
  price: string;
  is_in_stock: boolean;
};

export function ProductGrid({ products }: { products: Product[] }) {
  return (
    <section>
      {products.map((product) => (
        <ProductCard
          key={product.slug}
          name={product.name}
          slug={product.slug}
          price={product.price}
          inStock={product.is_in_stock}
        />
      ))}
    </section>
  );
}

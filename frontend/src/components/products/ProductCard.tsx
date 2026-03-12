type ProductCardProps = {
  name: string;
  slug: string;
  price: string;
  inStock: boolean;
};

export function ProductCard({ name, slug, price, inStock }: ProductCardProps) {
  return (
    <article>
      <h3>{name}</h3>
      <p>{price}</p>
      <p>{inStock ? "In stock" : "Out of stock"}</p>
      <a href={`/products/${slug}`}>View details</a>
    </article>
  );
}

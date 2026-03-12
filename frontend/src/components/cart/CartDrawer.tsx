import { CartItemRow } from "./CartItemRow";

type Cart = {
  items: Array<{ id: string; product_name: string; quantity: number; line_total: string }>;
};

export function CartDrawer({ cart, onRemove }: { cart: Cart; onRemove: (id: string) => void }) {
  return (
    <aside>
      <h3>Your cart</h3>
      {cart.items.map((item) => (
        <CartItemRow key={item.id} item={item} onRemove={onRemove} />
      ))}
    </aside>
  );
}

type CartItem = {
  id: string;
  product_name: string;
  quantity: number;
  line_total: string;
};

export function CartItemRow({ item, onRemove }: { item: CartItem; onRemove: (id: string) => void }) {
  return (
    <div>
      <strong>{item.product_name}</strong>
      <span>Qty: {item.quantity}</span>
      <span>Total: {item.line_total}</span>
      <button type="button" onClick={() => onRemove(item.id)}>
        Remove
      </button>
    </div>
  );
}

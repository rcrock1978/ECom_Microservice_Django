import Link from "next/link";

export default function AdminDashboardPage() {
  return (
    <section className="grid gap-3 sm:grid-cols-3">
      <Link href="/admin/products" className="rounded border p-4">Manage Products</Link>
      <Link href="/admin/coupons" className="rounded border p-4">Manage Coupons</Link>
      <Link href="/admin/orders" className="rounded border p-4">Manage Orders</Link>
    </section>
  );
}

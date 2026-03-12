"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";

type Coupon = { code: string; discount_type: string; discount_value: string };

export default function AdminCouponsPage() {
  const [coupons, setCoupons] = useState<Coupon[]>([]);

  useEffect(() => {
    apiRequest<{ data: Coupon[] }>("/api/v1/coupons/admin/coupons/")
      .then((response) => setCoupons(response.data))
      .catch(() => setCoupons([]));
  }, []);

  return (
    <section>
      <h2 className="text-xl font-semibold">Coupons</h2>
      <ul className="mt-3 space-y-2">
        {coupons.map((coupon) => (
          <li key={coupon.code} className="rounded border p-3">
            <Link href={`/admin/coupons/${coupon.code}`}>
              {coupon.code} — {coupon.discount_type} ({coupon.discount_value})
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

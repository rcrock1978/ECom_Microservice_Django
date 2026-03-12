"use client";

import { useState } from "react";
import { apiRequest } from "@/lib/api";

export default function AdminCouponDetailPage({ params }: { params: { id: string } }) {
  const [status, setStatus] = useState("");

  async function updateCoupon() {
    try {
      await apiRequest(`/api/v1/coupons/admin/coupons/${params.id}/`, {
        method: "PATCH",
        body: JSON.stringify({ discount_value: 10 }),
      });
      setStatus("Coupon updated");
    } catch {
      setStatus("Update failed");
    }
  }

  return (
    <section>
      <h2 className="text-xl font-semibold">Coupon {params.id}</h2>
      <button className="mt-3 rounded border px-3 py-1" onClick={updateCoupon}>Update</button>
      {status ? <p className="mt-3">{status}</p> : null}
    </section>
  );
}

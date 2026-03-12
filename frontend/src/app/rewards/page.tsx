"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import RewardSummaryCard from "@/components/ui/RewardSummaryCard";

type RewardSummary = {
  user_id: string;
  available_points: number;
  lifetime_earned_points: number;
};

type RewardTransaction = {
  id: string;
  transaction_type: string;
  points: number;
  reason: string;
};

export default function RewardsPage() {
  const [summary, setSummary] = useState<RewardSummary | null>(null);
  const [transactions, setTransactions] = useState<RewardTransaction[]>([]);

  useEffect(() => {
    apiRequest<{ data: RewardSummary }>("/api/v1/rewards/summary/")
      .then((response) => setSummary(response.data))
      .catch(() => setSummary(null));

    apiRequest<{ data: RewardTransaction[] }>("/api/v1/rewards/history/")
      .then((response) => setTransactions(response.data))
      .catch(() => setTransactions([]));
  }, []);

  if (!summary) {
    return <main className="mx-auto max-w-3xl p-6">Unable to load rewards.</main>;
  }

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-semibold">Rewards</h1>
      <div className="mt-4">
        <RewardSummaryCard
          availablePoints={summary.available_points}
          lifetimeEarnedPoints={summary.lifetime_earned_points}
        />
      </div>
      <section className="mt-6">
        <h2 className="text-lg font-semibold">Transactions</h2>
        <ul className="mt-3 space-y-2">
          {transactions.map((tx) => (
            <li key={tx.id} className="rounded border p-3 text-sm">
              <div>{tx.transaction_type}</div>
              <div>Points: {tx.points}</div>
              <div>{tx.reason}</div>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}

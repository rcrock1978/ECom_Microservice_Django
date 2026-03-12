type RewardSummaryCardProps = {
  availablePoints: number;
  lifetimeEarnedPoints: number;
};

export default function RewardSummaryCard({ availablePoints, lifetimeEarnedPoints }: RewardSummaryCardProps) {
  return (
    <section className="rounded border p-4">
      <h2 className="text-lg font-semibold">Reward Summary</h2>
      <p className="mt-2 text-sm">Available Points: {availablePoints}</p>
      <p className="text-sm">Lifetime Earned: {lifetimeEarnedPoints}</p>
    </section>
  );
}

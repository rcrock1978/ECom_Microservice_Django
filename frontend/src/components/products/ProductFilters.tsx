"use client";

type ProductFiltersProps = {
  query: string;
  onQueryChange: (value: string) => void;
};

export function ProductFilters({ query, onQueryChange }: ProductFiltersProps) {
  return (
    <div>
      <input value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Search products" />
    </div>
  );
}

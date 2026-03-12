export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="mx-auto max-w-6xl p-6">
      <header className="mb-6 border-b pb-4">
        <h1 className="text-2xl font-semibold">Admin</h1>
      </header>
      {children}
    </main>
  );
}

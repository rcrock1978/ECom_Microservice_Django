import { AuthProvider } from "@/lib/auth/context";
import { CartProvider } from "@/lib/cart/context";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <CartProvider>
            <Header />
            <main>{children}</main>
            <Footer />
          </CartProvider>
        </AuthProvider>
      </body>
    </html>
  );
}

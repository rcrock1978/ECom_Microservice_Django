"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth/context";

export default function ForgotPasswordPage() {
  const { forgotPassword } = useAuth();
  const [email, setEmail] = useState("ray@example.com");

  return (
    <div>
      <h2>Forgot password</h2>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <button type="button" onClick={() => forgotPassword(email)}>
        Send reset link
      </button>
    </div>
  );
}

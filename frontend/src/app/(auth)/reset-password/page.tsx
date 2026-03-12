"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth/context";

export default function ResetPasswordPage() {
  const { resetPassword } = useAuth();
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("EvenStronger123");

  return (
    <div>
      <h2>Reset password</h2>
      <input value={token} onChange={(e) => setToken(e.target.value)} placeholder="Token" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="New password" />
      <button type="button" onClick={() => resetPassword(token, password)}>
        Reset password
      </button>
    </div>
  );
}

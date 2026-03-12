"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth/context";

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState("ray@example.com");
  const [password, setPassword] = useState("StrongPass123");

  return (
    <div>
      <h2>Login</h2>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Password" />
      <button type="button" onClick={() => login(email, password)}>
        Sign in
      </button>
    </div>
  );
}

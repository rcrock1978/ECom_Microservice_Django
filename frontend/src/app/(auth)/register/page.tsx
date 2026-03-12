"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth/context";

export default function RegisterPage() {
  const { register } = useAuth();
  const [name, setName] = useState("Ray");
  const [email, setEmail] = useState("ray@example.com");
  const [password, setPassword] = useState("StrongPass123");

  return (
    <div>
      <h2>Register</h2>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Password" />
      <button type="button" onClick={() => register(name, email, password)}>
        Create account
      </button>
    </div>
  );
}

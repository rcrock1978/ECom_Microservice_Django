"use client";

import { createContext, useContext, useMemo, useState } from "react";
import { apiRequest } from "@/lib/api/client";

type AuthContextValue = {
  isAuthenticated: boolean;
  userEmail?: string;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (token: string, newPassword: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState<string | undefined>(undefined);

  async function login(email: string, password: string): Promise<void> {
    await apiRequest("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setAuthenticated(true);
    setUserEmail(email);
  }

  async function logout(): Promise<void> {
    await apiRequest("/api/v1/auth/logout", { method: "POST" });
    setAuthenticated(false);
    setUserEmail(undefined);
  }

  async function register(name: string, email: string, password: string): Promise<void> {
    await apiRequest("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password }),
    });
  }

  async function forgotPassword(email: string): Promise<void> {
    await apiRequest("/api/v1/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  }

  async function resetPassword(token: string, newPassword: string): Promise<void> {
    await apiRequest("/api/v1/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ token, new_password: newPassword }),
    });
  }

  const value = useMemo(
    () => ({ isAuthenticated, userEmail, login, logout, register, forgotPassword, resetPassword }),
    [isAuthenticated, userEmail],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const error = {
      code: body?.error?.code ?? `HTTP_${response.status}`,
      message: body?.error?.message ?? "Request failed",
      details: body?.error?.details,
      status: response.status,
    };
    throw new Error(JSON.stringify(error));
  }

  return response.json() as Promise<T>;
}

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export type LoginRequest = { email: string; password: string }
export type LoginResponse = { access_token: string; token_type: string }
export type SignupRequest = { name: string; email: string; password: string }
export type SignupResponse = { message: string }

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

async function request<T>(path: string, body: unknown): Promise<T> {
  let res: Response
  try {
    res = await fetch(`${API_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
  } catch {
    // Network or CORS failure — the request never reached the server.
    throw new ApiError(0, "Não foi possível conectar ao servidor.")
  }

  // FastAPI puts error text under `detail`; try to parse either way.
  const data = await res.json().catch(() => null)

  if (!res.ok) {
    const detail =
      data && typeof data.detail === "string"
        ? data.detail
        : "Ocorreu um erro. Tente novamente."
    throw new ApiError(res.status, detail)
  }

  return data as T
}

export function login(payload: LoginRequest): Promise<LoginResponse> {
  return request<LoginResponse>("/auth/login", payload)
}

export function signup(payload: SignupRequest): Promise<SignupResponse> {
  return request<SignupResponse>("/users", payload)
}

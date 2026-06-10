const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

const TOKEN_KEY = "auth_token"

export type LoginRequest = { email: string; password: string }
export type LoginResponse = { access_token: string; token_type: string }
export type SignupRequest = { name: string; email: string; password: string }
export type SignupResponse = { message: string }

export type TaskStatus = "TODO" | "IN_PROGRESS" | "COMPLETED"

export type Task = {
  id: number
  title: string
  user_id: number
  category: string | null
  status: TaskStatus
  start_date_time: string | null
  end_date_time: string | null
}

export type CreateTaskPayload = {
  title: string
  user_id: number
  category: string
  status?: TaskStatus
  start_date_time?: string | null
  end_date_time?: string | null
}

export type UpdateTaskPayload = {
  id: number
  title?: string | null
  user_id?: number | null
  category?: string | null
  status?: TaskStatus | null
  start_date_time?: string | null
  end_date_time?: string | null
}

export type Me = {
  id: number
  name: string
  email: string
  calendar_connected: boolean
}

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

type FetchOptions = {
  method?: "GET" | "POST" | "PUT" | "DELETE"
  body?: unknown
  auth?: boolean
}

async function apiFetch<T>(
  path: string,
  { method = "GET", body, auth = false }: FetchOptions = {}
): Promise<T> {
  const headers: Record<string, string> = {}
  if (body !== undefined) headers["Content-Type"] = "application/json"
  if (auth) {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token) headers["Authorization"] = `Bearer ${token}`
  }

  let res: Response
  try {
    res = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    })
  } catch {
    // Network or CORS failure — the request never reached the server.
    throw new ApiError(0, "Não foi possível conectar ao servidor.")
  }

  // 204 No Content (e.g. delete) has no body to parse.
  if (res.status === 204) return undefined as T

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
  return apiFetch<LoginResponse>("/auth/login", {
    method: "POST",
    body: payload,
  })
}

export function signup(payload: SignupRequest): Promise<SignupResponse> {
  return apiFetch<SignupResponse>("/users", { method: "POST", body: payload })
}

export function getMe(): Promise<Me> {
  return apiFetch<Me>("/users/me", { auth: true })
}

export function getTasks(): Promise<Task[]> {
  return apiFetch<Task[]>("/tasks", { auth: true })
}

export function createTask(
  payload: CreateTaskPayload
): Promise<{ message: string }> {
  return apiFetch("/tasks/", { method: "POST", body: payload, auth: true })
}

export function updateTask(payload: UpdateTaskPayload): Promise<Task> {
  return apiFetch<Task>(`/tasks/${payload.id}`, {
    method: "PUT",
    body: payload,
    auth: true,
  })
}

export function deleteTask(id: number): Promise<{ message: string }> {
  return apiFetch(`/tasks/${id}`, { method: "DELETE", auth: true })
}

export function getGoogleAuthUrl(): Promise<{ authorization_url: string }> {
  return apiFetch("/auth/google/authorize", { auth: true })
}

export function disconnectGoogle(): Promise<{ message: string }> {
  return apiFetch("/auth/google/disconnect", { method: "DELETE", auth: true })
}

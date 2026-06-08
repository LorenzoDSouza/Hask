import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { LoginForm } from "@/components/login-form"
import { login, ApiError } from "@/lib/api"
import { useAuth } from "@/lib/auth-context"

export function LoginPage() {
  const { setToken } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(values: { email: string; password: string }) {
    setLoading(true)
    setError(null)
    try {
      const res = await login(values)
      setToken(res.access_token)
      navigate("/", { replace: true })
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Erro ao entrar. Tente novamente."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh items-center justify-center p-6">
      <div className="w-full max-w-sm">
        <LoginForm onSubmit={handleSubmit} loading={loading} error={error} />
      </div>
    </div>
  )
}

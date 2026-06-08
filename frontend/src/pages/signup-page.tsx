import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { SignupForm } from "@/components/signup-form"
import { login, signup, ApiError } from "@/lib/api"
import { useAuth } from "@/lib/auth-context"

export function SignupPage() {
  const { setToken } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(values: {
    name: string
    email: string
    password: string
    confirmPassword: string
  }) {
    if (values.password !== values.confirmPassword) {
      setError("As senhas não coincidem.")
      return
    }

    setLoading(true)
    setError(null)
    try {
      await signup({
        name: values.name,
        email: values.email,
        password: values.password,
      })
      // Backend signup returns no token, so log in right after to get one.
      const res = await login({
        email: values.email,
        password: values.password,
      })
      setToken(res.access_token)
      navigate("/", { replace: true })
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Erro ao criar a conta. Tente novamente."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh items-center justify-center p-6">
      <div className="w-full max-w-sm">
        <SignupForm onSubmit={handleSubmit} loading={loading} error={error} />
      </div>
    </div>
  )
}

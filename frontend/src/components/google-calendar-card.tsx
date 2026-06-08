import { useState } from "react"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/lib/auth-context"
import {
  ApiError,
  disconnectGoogle,
  getGoogleAuthUrl,
} from "@/lib/api"

export function GoogleCalendarCard() {
  const { user, refreshUser } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleConnect() {
    setLoading(true)
    setError(null)
    try {
      // O endpoint exige header Bearer, por isso buscamos a URL via fetch
      // autenticado antes de redirecionar o browser para o Google.
      const { authorization_url } = await getGoogleAuthUrl()
      window.location.assign(authorization_url)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Erro ao conectar.")
      setLoading(false)
    }
  }

  async function handleDisconnect() {
    setLoading(true)
    setError(null)
    try {
      await disconnectGoogle()
      await refreshUser()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Erro ao desconectar.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-between rounded-lg border bg-card p-4 shadow-xs">
      <div>
        <p className="font-medium">Google Calendar</p>
        <p className="text-sm text-muted-foreground">
          {user?.calendar_connected
            ? "Tarefas com horário de início e fim viram eventos no seu calendário."
            : "Conecte para criar eventos automaticamente a partir das tarefas."}
        </p>
        {error && <p className="mt-1 text-xs text-destructive">{error}</p>}
      </div>
      {user?.calendar_connected ? (
        <Button
          variant="outline"
          size="sm"
          onClick={handleDisconnect}
          disabled={loading}
        >
          {loading ? "..." : "Desconectar"}
        </Button>
      ) : (
        <Button size="sm" onClick={handleConnect} disabled={loading}>
          {loading ? "..." : "Conectar"}
        </Button>
      )}
    </div>
  )
}

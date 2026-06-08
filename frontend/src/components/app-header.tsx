import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/lib/auth-context"
import { cn } from "@/lib/utils"

export function AppHeader() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/login", { replace: true })
  }

  return (
    <header className="flex items-center justify-between border-b px-6 py-4">
      <div className="flex items-center gap-3">
        <h1 className="text-lg font-bold">Hask</h1>
        <span
          className={cn(
            "rounded-full px-2 py-0.5 text-xs font-medium",
            user?.calendar_connected
              ? "bg-green-500/15 text-green-600 dark:text-green-400"
              : "bg-muted text-muted-foreground"
          )}
        >
          {user?.calendar_connected ? "Calendário conectado" : "Calendário desconectado"}
        </span>
      </div>
      <div className="flex items-center gap-3">
        {user && (
          <span className="text-sm text-muted-foreground">{user.name}</span>
        )}
        <Button variant="outline" size="sm" onClick={handleLogout}>
          Sair
        </Button>
      </div>
    </header>
  )
}

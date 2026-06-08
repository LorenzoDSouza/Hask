import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import { AppHeader } from "@/components/app-header"
import { GoogleCalendarCard } from "@/components/google-calendar-card"
import { TaskList } from "@/components/task-list"
import { useAuth } from "@/lib/auth-context"

export function HomePage() {
  const { user, refreshUser } = useAuth()
  const [searchParams, setSearchParams] = useSearchParams()
  const [notice, setNotice] = useState<{
    kind: "success" | "error"
    text: string
  } | null>(null)

  // Handle the redirect coming back from the Google OAuth callback.
  useEffect(() => {
    const calendar = searchParams.get("calendar")
    if (!calendar) return
    if (calendar === "connected") {
      setNotice({ kind: "success", text: "Google Calendar conectado!" })
      void refreshUser()
    } else if (calendar === "error") {
      setNotice({
        kind: "error",
        text: "Não foi possível conectar o Google Calendar.",
      })
    }
    searchParams.delete("calendar")
    setSearchParams(searchParams, { replace: true })
  }, [searchParams, setSearchParams, refreshUser])

  return (
    <div className="flex min-h-svh flex-col">
      <AppHeader />
      <main className="mx-auto w-full max-w-2xl flex-1 px-6 py-8">
        <div className="flex flex-col gap-6">
          {notice && (
            <div
              className={
                notice.kind === "success"
                  ? "rounded-md bg-green-500/15 px-4 py-2 text-sm text-green-700 dark:text-green-400"
                  : "rounded-md bg-destructive/15 px-4 py-2 text-sm text-destructive"
              }
            >
              {notice.text}
            </div>
          )}

          <GoogleCalendarCard />

          {user ? (
            <TaskList userId={user.id} />
          ) : (
            <p className="text-sm text-muted-foreground">Carregando...</p>
          )}
        </div>
      </main>
    </div>
  )
}

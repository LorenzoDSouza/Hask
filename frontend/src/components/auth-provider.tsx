import { useCallback, useMemo, useState } from "react"
import type { ReactNode } from "react"
import { AuthContext } from "@/lib/auth-context"

const TOKEN_KEY = "auth_token"

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(() =>
    localStorage.getItem(TOKEN_KEY)
  )

  const setToken = useCallback((next: string) => {
    localStorage.setItem(TOKEN_KEY, next)
    setTokenState(next)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setTokenState(null)
  }, [])

  const value = useMemo(
    () => ({ token, isAuthenticated: token !== null, setToken, logout }),
    [token, setToken, logout]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

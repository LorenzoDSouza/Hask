import { useCallback, useEffect, useMemo, useState } from "react"
import type { ReactNode } from "react"
import { AuthContext } from "@/lib/auth-context"
import { ApiError, getMe, type Me } from "@/lib/api"

const TOKEN_KEY = "auth_token"

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(() =>
    localStorage.getItem(TOKEN_KEY)
  )
  const [user, setUser] = useState<Me | null>(null)

  const setToken = useCallback((next: string) => {
    localStorage.setItem(TOKEN_KEY, next)
    setTokenState(next)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setTokenState(null)
    setUser(null)
  }, [])

  const refreshUser = useCallback(async () => {
    if (!localStorage.getItem(TOKEN_KEY)) return
    try {
      setUser(await getMe())
    } catch (err) {
      // Token invalid/expired
      if (err instanceof ApiError && err.status === 401) logout()
    }
  }, [logout])

  // Load the current user whenever we have a token.
  useEffect(() => {
    if (!token) return
    let active = true
    getMe()
      .then((me) => {
        if (active) setUser(me)
      })
      .catch((err) => {
        if (active && err instanceof ApiError && err.status === 401) logout()
      })
    return () => {
      active = false
    }
  }, [token, logout])

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: token !== null,
      user,
      setToken,
      refreshUser,
      logout,
    }),
    [token, user, setToken, refreshUser, logout]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

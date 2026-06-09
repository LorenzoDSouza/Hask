import { createContext, useContext } from "react"
import type { Me } from "@/lib/api"

export type AuthContextValue = {
  token: string | null
  isAuthenticated: boolean
  user: Me | null
  setToken: (token: string) => void
  refreshUser: () => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthContextValue | undefined>(
  undefined
)

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (ctx === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return ctx
}

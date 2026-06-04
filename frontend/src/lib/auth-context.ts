import { createContext, useContext } from "react"

export type AuthContextValue = {
  token: string | null
  isAuthenticated: boolean
  setToken: (token: string) => void
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

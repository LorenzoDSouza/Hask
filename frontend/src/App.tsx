import { Routes, Route } from "react-router-dom"
import { ProtectedRoute, PublicOnlyRoute } from "@/components/protected-route"
import { LoginPage } from "@/pages/login-page"
import { SignupPage } from "@/pages/signup-page"
import { HomePage } from "@/pages/home-page"

export function App() {
  return (
    <Routes>
      <Route element={<PublicOnlyRoute />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
      </Route>
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<HomePage />} />
      </Route>
    </Routes>
  )
}

export default App

import { useState } from "react"
import { Link } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

export type LoginFormProps = Omit<React.ComponentProps<"form">, "onSubmit"> & {
  onSubmit: (values: { email: string; password: string }) => void
  loading?: boolean
  error?: string | null
}

export function LoginForm({
  className,
  onSubmit,
  loading = false,
  error,
  ...props
}: LoginFormProps) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    onSubmit({ email, password })
  }

  return (
    <form
      className={cn("flex flex-col gap-6", className)}
      onSubmit={handleSubmit}
      {...props}
    >
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Entre na sua conta</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Informe seu e-mail abaixo para entrar na sua conta
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">E-mail</FieldLabel>
          <Input
            id="email"
            type="email"
            placeholder="m@exemplo.com"
            required
            className="bg-background"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
          />
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Senha</FieldLabel>
            <a
              href="#"
              className="ml-auto text-sm underline-offset-4 hover:underline"
            >
              Esqueceu sua senha?
            </a>
          </div>
          <Input
            id="password"
            type="password"
            required
            className="bg-background"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
          />
        </Field>
        <FieldError>{error}</FieldError>
        <Field>
          <Button type="submit" disabled={loading}>
            {loading ? "Entrando..." : "Entrar"}
          </Button>
          <FieldDescription className="text-center">
            Não tem uma conta?{" "}
            <Link to="/signup" className="underline underline-offset-4">
              Cadastre-se
            </Link>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}

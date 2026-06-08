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

export type SignupFormProps = Omit<React.ComponentProps<"form">, "onSubmit"> & {
  onSubmit: (values: {
    name: string
    email: string
    password: string
    confirmPassword: string
  }) => void
  loading?: boolean
  error?: string | null
}

export function SignupForm({
  className,
  onSubmit,
  loading = false,
  error,
  ...props
}: SignupFormProps) {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    onSubmit({ name, email, password, confirmPassword })
  }

  return (
    <form
      className={cn("flex flex-col gap-6", className)}
      onSubmit={handleSubmit}
      {...props}
    >
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Crie sua conta</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Preencha o formulário abaixo para criar sua conta
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="name">Nome completo</FieldLabel>
          <Input
            id="name"
            type="text"
            placeholder="João da Silva"
            required
            className="bg-background"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={loading}
          />
        </Field>
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
          <FieldDescription>
            Usaremos este e-mail para entrar em contato. Não compartilharemos
            seu e-mail com ninguém.
          </FieldDescription>
        </Field>
        <Field>
          <FieldLabel htmlFor="password">Senha</FieldLabel>
          <Input
            id="password"
            type="password"
            required
            className="bg-background"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
          />
          <FieldDescription>Deve ter pelo menos 8 caracteres.</FieldDescription>
        </Field>
        <Field>
          <FieldLabel htmlFor="confirm-password">Confirmar senha</FieldLabel>
          <Input
            id="confirm-password"
            type="password"
            required
            className="bg-background"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}
          />
          <FieldDescription>Confirme sua senha.</FieldDescription>
        </Field>
        <FieldError>{error}</FieldError>
        <Field>
          <Button type="submit" disabled={loading}>
            {loading ? "Criando conta..." : "Criar conta"}
          </Button>
          <FieldDescription className="px-6 text-center">
            Já tem uma conta?{" "}
            <Link to="/login" className="underline underline-offset-4">
              Entrar
            </Link>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}

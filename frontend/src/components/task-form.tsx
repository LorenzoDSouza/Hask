import { useState } from "react"
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import {
  ApiError,
  createTask,
  updateTask,
  type Task,
  type TaskStatus,
} from "@/lib/api"

const STATUS_OPTIONS: { value: TaskStatus; label: string }[] = [
  { value: "TODO", label: "A fazer" },
  { value: "IN_PROGRESS", label: "Em progresso" },
  { value: "COMPLETED", label: "Concluída" },
]

// "2026-06-05T10:00:00" -> "2026-06-05T10:00" (datetime-local input format)
function toInputValue(iso: string | null): string {
  if (!iso) return ""
  return iso.slice(0, 16)
}

// "2026-06-05T10:00" -> "2026-06-05T10:00:00" (or null when empty)
function toPayloadValue(value: string): string | null {
  if (!value) return null
  return value.length === 16 ? `${value}:00` : value
}

type TaskFormProps = {
  userId: number
  initial?: Task
  onSaved: () => void
  onCancel: () => void
}

export function TaskForm({ userId, initial, onSaved, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(initial?.title ?? "")
  const [category, setCategory] = useState(initial?.category ?? "")
  const [status, setStatus] = useState<TaskStatus>(initial?.status ?? "TODO")
  const [start, setStart] = useState(toInputValue(initial?.start_date_time ?? null))
  const [end, setEnd] = useState(toInputValue(initial?.end_date_time ?? null))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      if (initial) {
        await updateTask({
          id: initial.id,
          title,
          category,
          status,
          start_date_time: toPayloadValue(start),
          end_date_time: toPayloadValue(end),
        })
      } else {
        await createTask({
          title,
          user_id: userId,
          category,
          status,
          start_date_time: toPayloadValue(start),
          end_date_time: toPayloadValue(end),
        })
      }
      onSaved()
    } catch (err) {
      setError(
        err instanceof ApiError ? err.message : "Erro ao salvar a tarefa."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-lg border bg-card p-4 shadow-xs"
    >
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="title">Título</FieldLabel>
          <Input
            id="title"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={loading}
          />
        </Field>
        <Field>
          <FieldLabel htmlFor="category">Categoria</FieldLabel>
          <Input
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            disabled={loading}
          />
        </Field>
        <Field>
          <FieldLabel htmlFor="status">Status</FieldLabel>
          <select
            id="status"
            value={status}
            onChange={(e) => setStatus(e.target.value as TaskStatus)}
            disabled={loading}
            className={cn(
              "h-9 w-full rounded-md border border-input bg-transparent px-2.5 text-sm shadow-xs outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 disabled:opacity-50 dark:bg-input/30"
            )}
          >
            {STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </Field>
        <div className="flex gap-3">
          <Field>
            <FieldLabel htmlFor="start">Início</FieldLabel>
            <Input
              id="start"
              type="datetime-local"
              value={start}
              onChange={(e) => setStart(e.target.value)}
              disabled={loading}
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="end">Fim</FieldLabel>
            <Input
              id="end"
              type="datetime-local"
              value={end}
              onChange={(e) => setEnd(e.target.value)}
              disabled={loading}
            />
          </Field>
        </div>
        <FieldError>{error}</FieldError>
        <div className="flex justify-end gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={loading}
          >
            Cancelar
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? "Salvando..." : initial ? "Salvar" : "Criar tarefa"}
          </Button>
        </div>
      </FieldGroup>
    </form>
  )
}

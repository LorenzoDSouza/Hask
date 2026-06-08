import { useState } from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { ApiError, deleteTask, type Task, type TaskStatus } from "@/lib/api"

const STATUS_META: Record<TaskStatus, { label: string; className: string }> = {
  TODO: { label: "A fazer", className: "bg-muted text-muted-foreground" },
  IN_PROGRESS: {
    label: "Em progresso",
    className: "bg-blue-500/15 text-blue-600 dark:text-blue-400",
  },
  COMPLETED: {
    label: "Concluída",
    className: "bg-green-500/15 text-green-600 dark:text-green-400",
  },
}

function formatDateTime(iso: string | null): string | null {
  if (!iso) return null
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  })
}

type TaskItemProps = {
  task: Task
  onEdit: (task: Task) => void
  onChanged: () => void
}

export function TaskItem({ task, onEdit, onChanged }: TaskItemProps) {
  const [deleting, setDeleting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const meta = STATUS_META[task.status]
  const start = formatDateTime(task.start_date_time)
  const end = formatDateTime(task.end_date_time)

  async function handleDelete() {
    if (!window.confirm(`Excluir a tarefa "${task.title}"?`)) return
    setDeleting(true)
    setError(null)
    try {
      await deleteTask(task.id)
      onChanged()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Erro ao excluir.")
      setDeleting(false)
    }
  }

  return (
    <li className="flex items-start justify-between gap-3 rounded-lg border bg-card p-4 shadow-xs">
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium">{task.title}</span>
          <span
            className={cn(
              "rounded-full px-2 py-0.5 text-xs font-medium",
              meta.className
            )}
          >
            {meta.label}
          </span>
        </div>
        {task.category && (
          <p className="mt-1 text-sm text-muted-foreground">{task.category}</p>
        )}
        {(start || end) && (
          <p className="mt-1 text-xs text-muted-foreground">
            {start && <>Início: {start}</>}
            {start && end && " · "}
            {end && <>Fim: {end}</>}
          </p>
        )}
        {error && <p className="mt-1 text-xs text-destructive">{error}</p>}
      </div>
      <div className="flex shrink-0 gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(task)}
          disabled={deleting}
        >
          Editar
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={handleDelete}
          disabled={deleting}
        >
          {deleting ? "..." : "Excluir"}
        </Button>
      </div>
    </li>
  )
}

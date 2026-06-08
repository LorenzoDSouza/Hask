import { useCallback, useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { TaskItem } from "@/components/task-item"
import { TaskForm } from "@/components/task-form"
import { ApiError, getTasks, type Task } from "@/lib/api"

type TaskListProps = {
  userId: number
}

export function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  // null = panel closed, undefined = creating, Task = editing
  const [editing, setEditing] = useState<Task | null | undefined>(null)
  const showForm = editing !== null

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const all = await getTasks()
      setTasks(all.filter((t) => t.user_id === userId))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Erro ao carregar tarefas.")
    } finally {
      setLoading(false)
    }
  }, [userId])

  useEffect(() => {
    void load()
  }, [load])

  function handleSaved() {
    setEditing(null)
    void load()
  }

  return (
    <section className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Minhas tarefas</h2>
        {!showForm && (
          <Button size="sm" onClick={() => setEditing(undefined)}>
            Nova tarefa
          </Button>
        )}
      </div>

      {showForm && (
        <TaskForm
          userId={userId}
          initial={editing ?? undefined}
          onSaved={handleSaved}
          onCancel={() => setEditing(null)}
        />
      )}

      {loading && <p className="text-sm text-muted-foreground">Carregando...</p>}
      {error && <p className="text-sm text-destructive">{error}</p>}
      {!loading && !error && tasks.length === 0 && (
        <p className="text-sm text-muted-foreground">
          Nenhuma tarefa ainda. Crie a primeira!
        </p>
      )}

      <ul className="flex flex-col gap-3">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={(t) => setEditing(t)}
            onChanged={load}
          />
        ))}
      </ul>
    </section>
  )
}

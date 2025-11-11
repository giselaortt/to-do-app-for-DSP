import { useEffect, useState, type FormEvent } from "react"
import { TaskItem } from "./TaskItem"
import { TaskFormModal } from "./TaskFormModal"
import type { Task } from "../../../domain/task"
import { useAppContext } from "../../../main/AppContextProvider"

export const TaskList = () => {
	const { taskRepository } = useAppContext()
	const [tasks, setTasks] = useState<Task[]>([])
	const [isModalOpen, setIsModalOpen] = useState(false)
	const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
	const [draftTask, setDraftTask] = useState<Omit<Task, "id">>({
		title: "",
		description: "",
		status: "open",
	})

	const fetchTasks = async () => {
		const tasks = (await taskRepository.getAll()) as Task[]
		setTasks(tasks)
	}

	useEffect(() => {
		fetchTasks()
	}, [])

	const openCreateModal = () => {
		setDraftTask({
			title: "",
			description: "",
			status: "open",
		})
		setEditingTaskId(null)
		setIsModalOpen(true)
	}

	const openEditModal = (task: Task) => {
		setDraftTask({
			title: task.title,
			description: task.description,
			status: task.status,
		})
		setEditingTaskId(task.id)
		setIsModalOpen(true)
	}

	const closeModal = () => {
		setIsModalOpen(false)
		setEditingTaskId(null)
	}

	const handleDraftChange = (field: "title" | "description" | "status", value: string) => {
		setDraftTask((prev) => ({ ...prev, [field]: value }))
	}

	const handleSubmitTask = async (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault()
		if (!draftTask.title.trim()) {
			return
		}
		if (editingTaskId !== null) {
			await taskRepository.update(editingTaskId, draftTask)
		} else {
			await taskRepository.create(draftTask)
		}
		closeModal()
		fetchTasks()
	}

	const deleteTask = async (taskId: string) => {
		await taskRepository.delete(taskId)
		fetchTasks()
	}

	return (
		<div className="min-h-screen bg-slate-900 py-10">
			<div className="mx-auto w-full max-w-3xl rounded-lg bg-slate-800 px-6 py-8 shadow-lg">
				<header className="flex items-start justify-between gap-6">
					<div className="space-y-1">
						<h1 className="text-2xl font-semibold text-white">Task List</h1>
						<p className="text-sm text-slate-400">Manage your tasks quickly. Click on Add Task to create a new task.</p>
					</div>
					<button onClick={openCreateModal} className="rounded bg-emerald-500 px-4 py-2 text-sm font-semibold text-emerald-50">
						Add Task
					</button>
				</header>

				<section className="mt-6 space-y-3">
					{tasks.length === 0 ? (
						<div className="rounded border border-dashed border-slate-700 bg-slate-900 px-4 py-10 text-center text-slate-500">No tasks created yet.</div>
					) : (
						<ul className="space-y-3">
							{tasks.map((task) => (
								<TaskItem key={task.id} task={task} onEdit={() => openEditModal(task)} onDelete={() => deleteTask(task.id)} />
							))}
						</ul>
					)}
				</section>
			</div>
			<TaskFormModal isOpen={isModalOpen} editingTaskId={editingTaskId} draftTask={draftTask} onClose={closeModal} onDraftChange={handleDraftChange} onSubmit={handleSubmitTask} />
		</div>
	)
}

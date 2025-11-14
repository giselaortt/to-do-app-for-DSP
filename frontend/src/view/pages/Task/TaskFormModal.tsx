import { type FormEvent } from "react"
import type { Task } from "../../../domain/task"

type TaskDraft = Omit<Task, "id">

type TaskFormModalProps = {
	isOpen: boolean
	editingTaskId: string | null
	draftTask: TaskDraft
	onClose: () => void
	onDraftChange: (field: keyof TaskDraft, value: string) => void
	onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export const TaskFormModal = ({ isOpen, editingTaskId, draftTask, onClose, onDraftChange, onSubmit }: TaskFormModalProps) => {
	if (!isOpen) {
		return null
	}

	return (
		<div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 px-4">
			<div className="w-full max-w-md rounded-lg bg-slate-800 p-6 shadow-lg">
				<header className="mb-4 space-y-1">
					<h2 className="text-xl font-semibold text-white">{editingTaskId !== null ? "Edit task" : "Create a new task"}</h2>
					<p className="text-sm text-slate-400">{editingTaskId !== null ? "Update the task details and save your changes." : "Fill in the details below to add the task to your list."}</p>
				</header>
				<form onSubmit={onSubmit} className="space-y-4">
					<div>
						<label className="mb-1 block text-sm font-semibold text-slate-200" htmlFor="task-title">
							Title
						</label>
						<input id="task-title" name="title" type="text" value={draftTask.title} onChange={(event) => onDraftChange("title", event.target.value)} placeholder="Enter the task title" className="w-full rounded border border-slate-600 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/40" required />
					</div>
					<div>
						<label className="mb-1 block text-sm font-semibold text-slate-200" htmlFor="task-description">
							Description
						</label>
						<textarea id="task-description" name="description" value={draftTask.description} onChange={(event) => onDraftChange("description", event.target.value)} placeholder="Add context or steps for this task" rows={4} className="w-full rounded border border-slate-600 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/40" />
					</div>
					<div>
						<label className="mb-1 block text-sm font-semibold text-slate-200" htmlFor="task-status">
							Status
						</label>
						<select id="task-status" name="status" value={draftTask.status} onChange={(event) => onDraftChange("status", event.target.value)} className="w-full rounded border border-slate-600 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/40">
							<option value="open">Open</option>
							<option value="in_progress">In Progress</option>
							<option value="done">Done</option>
						</select>
					</div>
					<div className="flex items-center justify-end gap-2">
						<button type="button" onClick={onClose} className="rounded border border-slate-600 px-4 py-2 text-sm text-slate-200">
							Cancel
						</button>
						<button type="submit" className="rounded bg-emerald-500 px-4 py-2 text-sm font-semibold text-emerald-50">
							{editingTaskId !== null ? "Save Changes" : "Create Task"}
						</button>
					</div>
				</form>
			</div>
		</div>
	)
}

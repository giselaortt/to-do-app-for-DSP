import type { Task } from "../../../domain/task"

type Props = {
	task: Task
	onEdit: () => void
	onDelete: () => void
}

export const TaskItem = ({ task, onEdit, onDelete }: Props) => {
	return (
		<li key={task.id} className="flex justify-between gap-4 rounded-lg border border-slate-700 bg-slate-900 px-5 py-4">
			<div className="space-y-2">
				<h2 className="text-lg font-semibold text-white">{task.title}</h2>
				<p className="text-sm text-slate-400">{task.description}</p>
				<span className="inline-block rounded bg-slate-800 px-2 py-1 text-xs font-semibold uppercase text-slate-300">Status: {task.status}</span>
			</div>
			<div className="flex flex-col gap-2">
				<button onClick={onEdit} className="rounded border border-slate-600 px-3 py-1 text-xs font-semibold uppercase text-slate-200">
					Edit
				</button>
				<button onClick={onDelete} className="rounded border border-red-400 px-3 py-1 text-xs font-semibold uppercase text-red-300">
					Delete
				</button>
			</div>
		</li>
	)
}

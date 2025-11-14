export type TaskStatus = "open" | "in_progress" | "done"

export type Task = {
	id: string
	title: string
	description: string
	status: TaskStatus
}

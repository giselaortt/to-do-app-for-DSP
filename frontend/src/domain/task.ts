export type TaskStatus = "open" | "in_progress" | "completed"

export type Task = {
	id: string
	title: string
	description: string
	status: TaskStatus
}

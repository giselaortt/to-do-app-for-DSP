import type { Task } from "../../domain/task"

export class TaskRepository {
	private readonly baseUrl = "http://localhost:3000/api/tasks" // Changed from 3002 to 3000

	getAll = async () => {
		const tasks = await fetch(this.baseUrl)
		return tasks.json()
	}
	
	create = async (task: Omit<Task, "id">) => {
		const response = await fetch(this.baseUrl, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(task),
		})
		return response.json()
	}
	
	update = async (id: string, task: Partial<Task>) => {
		const response = await fetch(`${this.baseUrl}/${id}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(task),
		})
		return response.json()
	}
	
	delete = async (id: string) => {
		const response = await fetch(`${this.baseUrl}/${id}`, {
			method: "DELETE",
		})
		return response.status
	}
}

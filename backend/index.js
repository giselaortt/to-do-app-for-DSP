const express = require("express")
const cors = require("cors")

const app = express()
const PORT = process.env.PORT || 3000

app.use(express.json())
app.use(cors())

let tasks = [
	{ id: 1, title: "Task 1", description: "Description 1", status: "open" },
	{ id: 2, title: "Task 2", description: "Description 2", status: "in_progress" },
	{ id: 3, title: "Task 3", description: "Description 3", status: "completed" },
]

app.get("/api/tasks", (_req, res) => {
	res.json(tasks)
})

app.post("/api/tasks", (req, res) => {
	const { title, description } = req.body
	const newTask = { id: tasks.length + 1, title, description, status: "open" }
	tasks.push(newTask)
	res.status(201).json({ message: "Task created" })
})

app.put("/api/tasks/:id", (req, res) => {
	console.log(req.body)
	const { id } = req.params
	const { title, description } = req.body
	const task = tasks.find((task) => task.id === parseInt(id))
	if (!task) {
		return res.status(404).json({ message: "Task not found" })
	}
	task.title = title
	task.description = description
	res.status(202).json({ message: "Task updated" })
})

app.delete("/api/tasks/:id", (req, res) => {
	const { id } = req.params
	const task = tasks.find((task) => task.id === parseInt(id))
	if (!task) {
		return res.status(404).json({ message: "Task not found" })
	}
	tasks = tasks.filter((task) => task.id !== parseInt(id))
	res.status(203).json({ message: "Task deleted" })
})

app.listen(PORT, () => {
	console.log(`Server listening on http://localhost:${PORT}`)
})

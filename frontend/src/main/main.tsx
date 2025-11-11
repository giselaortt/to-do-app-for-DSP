import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import "./index.css"
import { AppContextProvider } from "./AppContextProvider"
import { TaskList } from "../view/pages/Task/TaskList"

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<AppContextProvider>
			<TaskList />
		</AppContextProvider>
	</StrictMode>
)

import { createContext, useContext } from "react"
import { TaskRepository } from "../infra/repository/TaskRepository"

type AppContextType = {
	taskRepository: TaskRepository
}

const AppContext = createContext<AppContextType>({} as AppContextType)

export const AppContextProvider = ({ children }: { children: React.ReactNode }) => {
	return <AppContext.Provider value={{ taskRepository: new TaskRepository() }}>{children}</AppContext.Provider>
}

export const useAppContext = () => {
	return useContext(AppContext)
}

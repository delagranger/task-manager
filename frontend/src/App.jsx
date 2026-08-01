import { useEffect, useState, useCallback } from "react";
import "./App.css";

import api from "./services/api";
import TaskList from "./components/TaskList";
import TaskForm from "./components/TaskForm";
import GroupList from "./components/GroupList";
import GroupForm from "./components/GroupForm";

const STATUSES = ["active", "frozen", "finished"];

function App() {
    const [tasks, setTasks] = useState([]);
    const [groups, setGroups] = useState([]);
    const [tab, setTab] = useState("tasks");

    const [taskSort, setTaskSort] = useState("id");
    const [groupSort, setGroupSort] = useState("id");
    const [filterStatus, setFilterStatus] = useState("");
    const [filterGroup, setFilterGroup] = useState("");

    const loadTasks = useCallback(async () => {
        try {
            const params = { sort_type: taskSort };
            if (filterStatus) {
                params.filtered = true;
                params.status = filterStatus;
            }
            if (filterGroup) {
                params.filtered = true;
                params.group = filterGroup;
            }
            const response = await api.get("/tasks/", { params });
            setTasks(response.data);
        } catch (error) {
            console.error("Load tasks error:", error);
        }
    }, [taskSort, filterStatus, filterGroup]);

    const loadGroups = useCallback(async () => {
        try {
            const response = await api.get("/groups/", {
                params: { sort_type: groupSort },
            });
            setGroups(response.data);
        } catch (error) {
            console.error("Load groups error:", error);
        }
    }, [groupSort]);

    useEffect(() => {
        loadTasks();
        loadGroups();
    }, [loadTasks, loadGroups]);

    const createTask = async (title, status, group) => {
        try {
            await api.post("/tasks/", { title, status, group });
            loadTasks();
            loadGroups();
        } catch (error) {
            console.error("Create task error:", error);
            alert(
                error.response?.data?.detail ||
                    "Failed to create task. Check title length (max 50) and group existence."
            );
        }
    };

    const updateTask = async (id, title, status, group) => {
        try {
            await api.patch(`/tasks/${id}/`, { title, status, group });
            loadTasks();
            loadGroups();
        } catch (error) {
            console.error("Update task error:", error);
            alert(
                error.response?.data?.detail ||
                    "Failed to update task."
            );
        }
    };

    const deleteTask = async (id) => {
        try {
            await api.delete(`/tasks/${id}/`);
            loadTasks();
            loadGroups();
        } catch (error) {
            console.error("Delete task error:", error);
            alert(
                error.response?.data?.detail ||
                    "Failed to delete task."
            );
        }
    };

    const createGroup = async (title) => {
        try {
            await api.post("/groups/", { title });
            loadGroups();
        } catch (error) {
            console.error("Create group error:", error);
            alert(
                error.response?.data?.detail ||
                    "Failed to create group. Check title length (max 25)."
            );
        }
    };

    const updateGroup = async (id, title) => {
        try {
            await api.patch(`/groups/${id}/`, { title });
            loadGroups();
            loadTasks();
        } catch (error) {
            console.error("Update group error:", error);
            alert(
                error.response?.data?.detail ||
                    "Failed to update group."
            );
        }
    };

    const deleteGroup = async (id) => {
        try {
            await api.delete(`/groups/${id}/`);
            loadGroups();
            loadTasks();
        } catch (error) {
            console.error("Delete group error:", error);
            alert(
                error.response?.data?.detail ||
                    "Failed to delete group."
            );
        }
    };

    return (
        <div className="app">
            <header className="app-header">
                <h1>Task Manager</h1>
                <nav className="tabs">
                    <button
                        className={`tab ${tab === "tasks" ? "active" : ""}`}
                        onClick={() => setTab("tasks")}
                    >
                        Tasks
                    </button>
                    <button
                        className={`tab ${tab === "groups" ? "active" : ""}`}
                        onClick={() => setTab("groups")}
                    >
                        Groups
                    </button>
                </nav>
            </header>

            <main className="app-main">
                {tab === "tasks" && (
                    <section className="tasks-section">
                        <div className="section-header">
                            <h2>Tasks</h2>
                            <div className="controls">
                                <select
                                    value={taskSort}
                                    onChange={(e) =>
                                        setTaskSort(e.target.value)
                                    }
                                >
                                    <option value="id">Sort by ID</option>
                                    <option value="title">
                                        Sort by Title
                                    </option>
                                    <option value="status">
                                        Sort by Status
                                    </option>
                                    <option value="group_id">
                                        Sort by Group
                                    </option>
                                </select>
                                <select
                                    value={filterStatus}
                                    onChange={(e) =>
                                        setFilterStatus(e.target.value)
                                    }
                                >
                                    <option value="">All statuses</option>
                                    {STATUSES.map((s) => (
                                        <option key={s} value={s}>
                                            {s}
                                        </option>
                                    ))}
                                </select>
                                <select
                                    value={filterGroup}
                                    onChange={(e) =>
                                        setFilterGroup(e.target.value)
                                    }
                                >
                                    <option value="">All groups</option>
                                    {groups.map((g) => (
                                        <option key={g.id} value={g.title}>
                                            {g.title}
                                        </option>
                                    ))}
                                </select>
                                <button
                                    onClick={() => {
                                        setFilterStatus("");
                                        setFilterGroup("");
                                    }}
                                >
                                    Clear Filters
                                </button>
                            </div>
                        </div>

                        <TaskForm
                            onSubmit={createTask}
                            groups={groups}
                            statuses={STATUSES}
                        />

                        <TaskList
                            tasks={tasks}
                            onDelete={deleteTask}
                            onUpdate={updateTask}
                            groups={groups}
                            statuses={STATUSES}
                        />
                    </section>
                )}

                {tab === "groups" && (
                    <section className="groups-section">
                        <div className="section-header">
                            <h2>Groups</h2>
                            <select
                                value={groupSort}
                                onChange={(e) =>
                                    setGroupSort(e.target.value)
                                }
                            >
                                <option value="id">Sort by ID</option>
                                <option value="title">Sort by Title</option>
                            </select>
                        </div>

                        <GroupForm onSubmit={createGroup} />

                        <GroupList
                            groups={groups}
                            onDelete={deleteGroup}
                            onUpdate={updateGroup}
                        />
                    </section>
                )}
            </main>
        </div>
    );
}

export default App;
import { useState } from "react";
import ConfirmModal from "./ConfirmModal";

function TaskList({ tasks, onDelete, onUpdate, groups, statuses }) {
    const [editingId, setEditingId] = useState(null);
    const [editTitle, setEditTitle] = useState("");
    const [editStatus, setEditStatus] = useState("active");
    const [editGroup, setEditGroup] = useState("");
    const [deleteTarget, setDeleteTarget] = useState(null);

    if (!tasks || tasks.length === 0) {
        return <p className="empty-msg">No tasks found.</p>;
    }

    const startEdit = (task) => {
        setEditingId(task.id);
        setEditTitle(task.title);
        setEditStatus(task.status);
        setEditGroup(task.group);
    };

    const cancelEdit = () => {
        setEditingId(null);
    };

    const saveEdit = (id) => {
        onUpdate(id, editTitle, editStatus, editGroup);
        setEditingId(null);
    };

    return (
        <table className="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Status</th>
                    <th>Group</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {tasks.map((task) =>
                    editingId === task.id ? (
                        <tr key={task.id} className="editing-row">
                            <td>{task.id}</td>
                            <td>
                                <input
                                    type="text"
                                    value={editTitle}
                                    maxLength={50}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    className="inline-input"
                                />
                            </td>
                            <td>
                                <select
                                    value={editStatus}
                                    onChange={(e) => setEditStatus(e.target.value)}
                                    className="inline-select"
                                >
                                    {statuses.map((s) => (
                                        <option key={s} value={s}>
                                            {s}
                                        </option>
                                    ))}
                                </select>
                            </td>
                            <td>
                                <select
                                    value={editGroup}
                                    onChange={(e) => setEditGroup(e.target.value)}
                                    className="inline-select"
                                >
                                    <option value="default group">default group</option>
                                    {groups.map((g) => (
                                        <option key={g.id} value={g.title}>
                                            {g.title}
                                        </option>
                                    ))}
                                </select>
                            </td>
                            <td className="actions-cell">
                                <button
                                    className="btn btn-primary btn-sm"
                                    onClick={() => saveEdit(task.id)}
                                >
                                    Save
                                </button>
                                <button
                                    className="btn btn-cancel btn-sm"
                                    onClick={cancelEdit}
                                >
                                    Cancel
                                </button>
                            </td>
                        </tr>
                    ) : (
                        <tr key={task.id}>
                            <td>{task.id}</td>
                            <td>{task.title}</td>
                            <td>
                                <span className={`status-badge status-${task.status}`}>
                                    {task.status}
                                </span>
                            </td>
                            <td>{task.group}</td>
                            <td className="actions-cell">
                                <button
                                    className="btn btn-edit"
                                    onClick={() => startEdit(task)}
                                >
                                    Edit
                                </button>
                                <button
                                    className="btn btn-delete"
                                    onClick={() => setDeleteTarget(task)}
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    )
                )}
            </tbody>

            {deleteTarget && (
                <ConfirmModal
                    message={`Delete task "${deleteTarget.title}"?`}
                    onConfirm={() => {
                        onDelete(deleteTarget.id);
                        setDeleteTarget(null);
                    }}
                    onCancel={() => setDeleteTarget(null)}
                />
            )}
        </table>
    );
}

export default TaskList;
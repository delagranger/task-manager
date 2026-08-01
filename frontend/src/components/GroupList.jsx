import { useState } from "react";
import ConfirmModal from "./ConfirmModal";

function GroupList({ groups, onDelete, onUpdate }) {
    const [editingId, setEditingId] = useState(null);
    const [editTitle, setEditTitle] = useState("");
    const [deleteTarget, setDeleteTarget] = useState(null);

    if (!groups || groups.length === 0) {
        return <p className="empty-msg">No groups found.</p>;
    }

    const startEdit = (group) => {
        setEditingId(group.id);
        setEditTitle(group.title);
    };

    const cancelEdit = () => {
        setEditingId(null);
    };

    const saveEdit = (id) => {
        onUpdate(id, editTitle);
        setEditingId(null);
    };

    return (
        <table className="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Tasks</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {groups.map((group) =>
                    editingId === group.id ? (
                        <tr key={group.id} className="editing-row">
                            <td>{group.id}</td>
                            <td>
                                <input
                                    type="text"
                                    value={editTitle}
                                    maxLength={25}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    className="inline-input"
                                />
                            </td>
                            <td>
                                {group.tasks && group.tasks.length > 0
                                    ? group.tasks.join(", ")
                                    : "—"}
                            </td>
                            <td className="actions-cell">
                                <button
                                    className="btn btn-primary btn-sm"
                                    onClick={() => saveEdit(group.id)}
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
                        <tr key={group.id}>
                            <td>{group.id}</td>
                            <td>{group.title}</td>
                            <td>
                                {group.tasks && group.tasks.length > 0
                                    ? group.tasks.join(", ")
                                    : "—"}
                            </td>
                            <td className="actions-cell">
                                <button
                                    className="btn btn-edit"
                                    onClick={() => startEdit(group)}
                                >
                                    Edit
                                </button>
                                <button
                                    className="btn btn-delete"
                                    onClick={() => setDeleteTarget(group)}
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
                    message={`Delete group "${deleteTarget.title}"?`}
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

export default GroupList;
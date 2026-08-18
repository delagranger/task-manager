import { useState } from "react";

function TaskForm({ onSubmit, onCancel, groups, statuses, initial }) {
    const [title, setTitle] = useState(initial?.title || "");
    const [status, setStatus] = useState(initial?.status || "active");
    const [group, setGroup] = useState(initial?.group || "");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!title.trim()) return;
        onSubmit(title.trim(), status, group || "default group");
        if (!initial) {
            setTitle("");
            setStatus("active");
            setGroup("");
        }
    };

    return (
        <form className="form" onSubmit={handleSubmit}>
            <h3>{initial ? "Edit Task" : "New Task"}</h3>
            <div className="form-row">
                <input
                    type="text"
                    placeholder="Task title (max 50)"
                    maxLength={50}
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
                <select value={status} onChange={(e) => setStatus(e.target.value)}>
                    {statuses.map((s) => (
                        <option key={s} value={s}>
                            {s}
                        </option>
                    ))}
                </select>
                <select value={group} onChange={(e) => setGroup(e.target.value)}>
                    <option value="">default group</option>
                    {groups.map((g) => (
                        <option key={g.id} value={g.title}>
                            {g.title}
                        </option>
                    ))}
                </select>
                <button type="submit" className="btn btn-primary">
                    {initial ? "Update" : "Create"}
                </button>
                {onCancel && (
                    <button type="button" className="btn btn-cancel" onClick={onCancel}>
                        Cancel
                    </button>
                )}
            </div>
        </form>
    );
}

export default TaskForm;
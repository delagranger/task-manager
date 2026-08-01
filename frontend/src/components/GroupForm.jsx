import { useState } from "react";

function GroupForm({ onSubmit, onCancel, initial }) {
    const [title, setTitle] = useState(initial?.title || "");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!title.trim()) return;
        onSubmit(title.trim());
        if (!initial) {
            setTitle("");
        }
    };

    return (
        <form className="form" onSubmit={handleSubmit}>
            <h3>{initial ? "Edit Group" : "New Group"}</h3>
            <div className="form-row">
                <input
                    type="text"
                    placeholder="Group title (max 25)"
                    maxLength={25}
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
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

export default GroupForm;
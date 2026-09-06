class Task:
    title: str
    status: str
    id: int | None
    group: str
    priority: str | None

    def __init__(
        self, title: str, status: str, group: str, id: int | None = None, priority: str | None = None
    ):
        self.title = title
        self.status = status
        self.id = id
        self.group = group
        self.priority = priority


    def __repr__(self) -> str:
        return f"Task(Title={self.title}, status={self.status}, group={self.group}, priority={self.priority})"

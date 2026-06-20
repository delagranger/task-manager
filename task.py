class Task:
    title: str
    status: str
    id: int | None
    group: str

    def __init__(self, title: str, status: str, group: str, id: int | None = None):
        self.title = title
        self.status = status
        self.id = id
        self.group = group


    def __repr__(self) -> str:
        return f"Task(Title={self.title}, status={self.status}, group={self.group})"



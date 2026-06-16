class Task:
    title: str
    status: str
    id: int | None
    group = str | None

    def __init__(self, title, status, id=None, group=None):
        self.title = title
        self.status = status
        self.id = id
        self.group = group


    def __repr__(self):
        return f"Task(Title={self.title}, status={self.status}, group={self.group})"



class Group:
    title: str
    id: int | None
    tasks: list | None


    def __init__(self, title, id=None, tasks=None):
        self.title = title
        self.id = id
        self.tasks = tasks


    def __repr__(self):
        return f"Group(Title={self.title})"


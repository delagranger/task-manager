class Group:
    title: str
    id: int | None
    tasks: list[str] | None


    def __init__(self, title: str, id: int | None = None, tasks: list[str] | None = None):
        self.title = title
        self.id = id
        self.tasks = tasks


    def __repr__(self) -> str:
        return f"Group(Title={self.title})"


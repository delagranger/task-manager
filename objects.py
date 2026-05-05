class Task:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def to_dict(self):
        task_to_dict = {"title": self.title, "id": self.id}
        return task_to_dict

    @classmethod
    def from_dict(cls, task_dict):
        task_obj = cls(task_dict["title"], task_dict["id"])
        return task_obj

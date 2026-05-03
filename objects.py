class Task:
    def __init__(self, title):
        self.title = title
    
    def to_dict(self):
        task_to_dict = {"title": self.title}
        return task_to_dict

    @classmethod
    def from_dict(cls, task_dict):
        task_obj = cls(task_dict["title"])
        return task_obj

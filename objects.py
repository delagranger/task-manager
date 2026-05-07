class Task:
    def __init__(self, title, id, status):
        self.title = title
        self.id = id
        self.status = status

    def to_dict(self):
        task_to_dict = {"title": self.title, 
                        "id": self.id,
                        "status": self.status
                        }
        return task_to_dict

    @classmethod
    def from_dict(cls, task_dict):
        task_obj = cls(task_dict["title"], 
                       task_dict["id"],
                       task_dict["status"])
        return task_obj

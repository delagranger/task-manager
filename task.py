class Task:
    def __init__(self, title, id, status, group):
        self.title = title
        self.id = id
        self.status = status
        self.group = group

    def to_dict(self):
        task_to_dict = {"title": self.title, 
                        "id": self.id, 
                        "status": self.status, 
                        "group": self.group,
        }
        return task_to_dict



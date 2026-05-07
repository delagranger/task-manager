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
                        "group": self.group
                        }
        return task_to_dict

    @classmethod
    def from_dict(cls, task_dict):
        task_obj = cls(task_dict["title"], 
                       task_dict["id"],
                       task_dict["status"],
                       task_dict["group"]
                       )
        return task_obj

class Group:
    def __init__(self, title, id):
        self.title = title
        self.id = id
    
    def to_dict(self):
        group_to_dict = {"title": self.title, "id": self.id}
        return group_to_dict
    
    @classmethod
    def from_dict(cls, group_dict):
        group_obj = cls(group_dict["title"], group_dict["id"])
        return group_obj
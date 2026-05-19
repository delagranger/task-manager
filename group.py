class Group:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def to_dict(self):
        group_to_dict = {"title": self.title, 
                         "id": self.id,
        }
        return group_to_dict

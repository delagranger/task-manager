class Group:
    def __init__(self, title):
        self.title = title
    
    
    def __str__(self):
        return "Type - Group; Title: %s;" % (self.title)
    

    def __repr__(self):
        return "Type - Group; Title=%r;" % (self.title)


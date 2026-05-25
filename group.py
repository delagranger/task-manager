class Group:
    def __init__(self, title):
        self.title = title
    
    @classmethod
    def print_group(self, group):
        print(f"""
                ГРУППА: {group[1]}
                ID: {group[0]}
        """)


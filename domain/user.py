class User:
    login: str
    password: str

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def __repr__(self) -> str:
        return f"User(Login={self.login})"

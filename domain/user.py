class User:
    login: str
    password: str

    def __init__(self, login: str, password_hash: str):
        self.login = login
        self.password_hash = password_hash

    def __repr__(self) -> str:
        return f"User(Login={self.login})"

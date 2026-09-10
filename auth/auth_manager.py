import logging

from domain import User
from repository import ORMManager
from exceptions import IncorrectLength, DifferentPasswords

log = logging.getLogger(__name__)

MAX_LOGIN_LENGTH = 20
MAX_PASSWORD_LENGTH = 20

class AuthManager:
    def __int__(self):
        self._orm_manager = ORMManager()

    def register(self, login: str, passwords: list):
        login = self._ensure_length_is_correct("login", login)

        password = self._compare_passwords(passwords)
        password = self._ensure_length_is_correct("password", password)
        # password_hash = self._hash_password(password)
        
        user = User(login, password)
        id, login = self._orm_manager.add_user(user)

        return id, login

    def _hash_password(self, password: str):
        pass

    def _compare_passwords(self, passwords: list):
        if passwords[0] != passwords[1]:
            log.error("Compare passwords: FAILED;")
            raise DifferentPasswords()
        else:
            log.debug("Compare passwords: SUCCESS;")
            return passwords[1]

    def _ensure_length_is_correct(self, obj_type: str, obj: str):
        cur_length = len(obj)
        if obj_type == "login" and cur_length > MAX_LOGIN_LENGTH:
            max_length = MAX_LOGIN_LENGTH
            log.error(
                "Ensure login is correct: FAILED; "
                "Login=%r, length=%r",
                obj, cur_length,
            )
            raise IncorrectLength(obj_type, cur_length, max_length)
        elif obj_type == "password" and cur_length > MAX_PASSWORD_LENGTH:
            max_length = MAX_PASSWORD_LENGTH
            log.error(
                "Ensure password is correct: FAILED; "
                "Password=%r, length=%r",
                obj, cur_length,
            )
            raise IncorrectLength(obj_type, cur_length, max_length)
        else:
            log.debug(
                "Ensure %s length is correct: SUCCESS; Length=%r",
                obj_type, cur_length,
            )
            return obj, cur_length



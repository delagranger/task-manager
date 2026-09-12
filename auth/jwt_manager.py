from datetime import datetime, timezone, timedelta
from pathlib import Path
import logging
import json
import jwt

from config import get_jwt_token_validity_period, get_jwt_secret_key

log = logging.getLogger(__name__)

JWT_ALGORITHM = "HS256"
JWT_PATH = Path("auth.json")

class JWTManager:
    def __init__(self):
        self._token_validity_period = get_jwt_token_validity_period()
        self._secret_key = get_jwt_secret_key()

    def create_jwt(self, id: int):
        claims = self._create_jwt_claims(id)
        token = jwt.encode(claims, self._secret_key, algorithm=(JWT_ALGORITHM))
        self._save_token(id, token)
        return id

    def read_jwt(self):
        path = JWT_PATH
        data = json.loads(path.read_text(encoding="utf-8"))
        jwt_data = jwt.decode(data["token"], self._secret_key, algorithms=JWT_ALGORITHM)
        id = int(jwt_data["sub"])
        return id

    def _create_jwt_claims(self, id):
        claims = {
            "sub": str(id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self._token_validity_period)
        }
        log.debug("Create JWT claims: SUCCESS;")
        return claims

    def _save_token(self, id, token):
        path = JWT_PATH
        data = {
            "id": id,
            "token": token
        }
        path.write_text(json.dumps(data), encoding="utf-8")
        log.debug("Save JWT: SUCCESS;")
import jwt
from datetime import datetime, timezone, timedelta
import logging
from config.config import get_jwt_token_validity_period, get_jwt_secret_key

log = logging.getLogger(__name__)

class JWTManager:
    def __init__(self):
        self._token_validity_period = get_jwt_token_validity_period()
        self._secret_key = get_jwt_secret_key()

    def create_jwt(self, id: int):
        claims = self._create_jwt_claims(id)
        token = jwt.encode(claims, self._secret_key, algorithm="HS256")
        self._save_token(token)

    def _create_jwt_claims(self, id):
        claims = {
            "sub": id,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self._token_validity_period)
        }
        return claims

    def _save_token(self, token):
        print(token)
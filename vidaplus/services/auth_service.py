from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt

from vidaplus.main.exceptions import ExpiredTokenError, InvalidTokenError, TokenRefreshError
from vidaplus.main.schemas.auth import TokenData
from vidaplus.settings import Settings


class AuthService:
    settings = Settings()

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        to_encode['id'] = str(data['id'])
        to_encode['created_at'] = data['created_at'].isoformat()
        expire = datetime.now(ZoneInfo(cls.settings.TIMEZONE)) + timedelta(
            minutes=cls.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, cls.settings.SECRET_KEY, algorithm=cls.settings.ALGORITHM)

    @classmethod
    def decode_access_token(cls, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, cls.settings.SECRET_KEY, algorithms=[cls.settings.ALGORITHM])
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError()
        except jwt.DecodeError:
            raise InvalidTokenError()

    @classmethod
    def refresh_token(cls, access_token: str) -> str:
        try:
            payload = cls.decode_access_token(access_token)

            if payload.exp < datetime.now(ZoneInfo(cls.settings.TIMEZONE)):
                raise ExpiredTokenError()

            new_access_token = cls.create_access_token(payload.model_dump())
            return new_access_token
        except Exception:
            raise TokenRefreshError()

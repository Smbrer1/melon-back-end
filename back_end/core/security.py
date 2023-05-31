from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt
from passlib.context import CryptContext

from back_end.core.config import settings
from back_end.models.user_model import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(subject: Union[User, Any], expires_delta: int = None) -> str:
    """ Функция создания access токена

    Args:
        subject: Объект шифруемый в JWT токене (UUID юзера)
        expires_delta: Дата окончания действия токена

    Returns: строку токена

    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta  # noqa
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            # TODO сделать отдельную функцию с другим экспайром для рефреша
        )

    to_encode = {"exp": expires_delta, "user": {
        "userId": str(subject.user_id),
        "username": subject.username,
        "phoneNumber": subject.phone_number,
        "email": subject.email,
        "firstName": subject.first_name,
        "lastName": subject.last_name,
        "disabled": subject.disabled
    }}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def get_password(password: str) -> str:
    """ Функция хеширования пароля

    Args:
        password: Строка пароля

    Returns: Хеш строка

    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """ Функция проверки 2-х хешей

    Args:
        password: Строка пароля
        hashed_pass: Строка захешированного пароля

    Returns: True/False

    """
    return password_context.verify(password, hashed_pass)

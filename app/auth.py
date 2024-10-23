from sqlalchemy.exc import SQLAlchemyError
from app.error_handling import HttpError
from app.models.models import  User
from flask import request




def protected_route(func):
    def wrapper(*args, **kwargs):
        try:
            headers = request.headers

            headers_token = headers.get("Token")
            if not headers_token:
                raise HttpError(401, "Токен не предоставлен")

            token = request.session.query(User).filter(
                User.token == headers_token).first()

            if token is None:
                raise HttpError(404, "Токен не найден")
            user_id = token.id

        except SQLAlchemyError:
            raise HttpError(500, "Ошибка базы данных")
        result = func(user_id, **kwargs)

        return result

    return wrapper
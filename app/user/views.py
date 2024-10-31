from sqlalchemy.exc import SQLAlchemyError

from app.error_handling import HttpError
from app.models.models import User
from flask import request


from flask import jsonify


def add_user():
    try:
        json_data = request.json
        if not json_data or 'login' not in json_data:
            raise  HttpError(400,"Введены некорректные данные")
        new_user = User(**json_data)
        request.session.add(new_user)
        request.session.commit()
        return jsonify(new_user.dict)
    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")

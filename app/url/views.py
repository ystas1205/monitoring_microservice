import pydantic
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.testing.suite.test_reflection import users

from app.auth import protected_route
from app.error_handling import HttpError
from app.models.models import Url, Events
from flask import request

from flask import jsonify

from app.url.shema import CreateUrl

from app.validators import validate


@protected_route
def add_url(*args, **kwargs):
    try:
        user_id = args[0]
        json_data = validate(CreateUrl, request.json)

        new_url = Url(path=json_data['path'], user_id=user_id)

        request.session.add(new_url)
        request.session.commit()
        return jsonify(new_url.dict)
    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")


@protected_route
def get_url(*args, **kwargs):
    try:
        user_id = args[0]
        urls = request.session.query(Url).filter(Url.user_id == user_id).all()
        urls_list = [url.dict for url in urls]
        return jsonify(urls_list)
    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")


@protected_route
def remove_url(*args, **kwargs):
    try:
        user_id = args[0]
        user_id_UUID = kwargs.get("url_id")
        target_UUID = kwargs.get("url_id")
        urls = request.session.get(Url, user_id_UUID)
        if urls is None:
            raise HttpError(404, "Url не найден")
        events = request.session.query(Events).filter(
            Events.url_id == target_UUID).all()
        for event in events:
            event.active = False
        if user_id != urls.user_id:
            raise HttpError(403, "У вас нет прав доступа к этому ресурсу")

        request.session.delete(urls)
        request.session.commit()
        return jsonify({"status": "delete"})
    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")

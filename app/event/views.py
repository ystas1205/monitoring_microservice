from celery.worker.state import total_count
from flask import request, jsonify
from redis.commands.search.reducers import count
from requests import session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.auth import protected_route
from app.error_handling import HttpError
from app.models.models import Events

@protected_route
def get_events(*args, **kwargs):
    try:
        url_id = kwargs.get("url_id")
        # query_parameters = request.args
        skip = request.args.get("skip")
        limit = request.args.get("limit")

        if skip is None or limit is None:
            raise HttpError(400, "Неверные параметры запроса")

        events_query = request.session.query(Events).filter(
            Events.url_id == url_id).limit(limit).offset(skip)
        events = events_query.all()

        total_count_query = request.session.query(func.count(Events.id)).filter(
            Events.url_id == url_id)
        total_count = total_count_query.scalar()

        result = [{"items": event.dict} for event in events]
        response = {"items": result,
                    "total_count": total_count}

        return jsonify(response)
    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")

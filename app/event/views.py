from celery.bin.result import result
from celery.worker.state import total_count
from flask import request, jsonify, url_for
from redis.commands.search.reducers import count
from requests import session
from sqlalchemy import func, case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.testing.pickleable import Order

from app.auth import protected_route
from app.error_handling import HttpError
from app.models.models import Events


@protected_route
def get_events(*args, **kwargs):
    try:

        url_id = kwargs.get("url_id")

        # получение query параметров
        # query_parameters = request.args

        skip = request.args.get("skip")
        limit = request.args.get("limit")

        if skip is None or limit is None:
            raise HttpError(400, "Неверные параметры запроса")

        events_query = request.session.query(Events).filter(
            Events.url_id == url_id).limit(limit).offset(skip)
        events = events_query.all()

        total_count_query = request.session.query(
            func.count(Events.id)).filter(
            Events.url_id == url_id)
        total_count = total_count_query.scalar()

        result = [{"items": event.dict} for event in events]
        response = {"items": result,
                    "total_count": total_count}

        return jsonify(response)
    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")


@protected_route
def monitoring_statistics(*args, **kwargs):
    try:

        # Получаем параметры запроса
        status_code = request.args.get("status_code")
        response_time = request.args.get("response_time")
        sort = request.args.get("sort")

        # Проверка на допустимые параметры сортировки
        if sort not in (
                'created', 'response_time', 'status_code',
                'response_size', '-created'):
            raise HttpError(400, "Неверные параметры запроса")

        # Проверка на наличие status_code и его корректность
        if status_code:
            list_status_code = status_code.split()
            if len(list(response_time.split(','))) != 2 or not all(
                    part.strip().isdigit() for part in list_status_code):
                raise HttpError(400, "Неверные параметры запроса")
        # Проверка на наличие response_time и sort
        if response_time is None or sort is None:
            raise HttpError(400,
                            "Неверные параметры запроса: response_time и sort обязательны")

        # Разбиение response_time на части и проверка корректности

        response_time_parts = response_time.split(',')

        if len(list(response_time.split(','))) != 2 or not all(
                part.strip().isdigit() for part in response_time_parts):
            raise HttpError(400, "Неверные параметры запроса")

        # Преобразование строк в целые числа
        try:
            response_time_1 = int(response_time_parts[0])
            response_time_2 = int(response_time_parts[1])
        except ValueError:
            raise HttpError(400,
                            "Неверные параметры запроса: значения response_time должны быть целыми числами.")
        # Формирование запроса к базе данных
        if status_code is not None:

            query = request.session.query(
                Events.url_id,
                func.avg(Events.response_time).label('avg_response_time'),

                func.max(Events.response_size).label('max_response_size'),

                func.count().label('total_events'),

                # Подсчет количества 2xx кодов
                func.count(case(
                    (Events.status_code.between(200, 299), 1),
                )).label('count_2xx'),

                # Подсчет количества 3xx кодов
                func.count(case(
                    (Events.status_code.between(300, 399), 1),
                )).label('count_3xx')

            ).filter(
                Events.status_code == status_code,
                Events.response_time.between(response_time_1, response_time_2),

            ).group_by(
                Events.url_id
            )

        else:

            # Запрос, когда status_code не предоставлен

            query = request.session.query(
                Events.url_id,
                func.avg(Events.response_time).label('avg_response_time'),
                func.max(Events.response_size).label('max_response_size'),
                func.count().label('total_events'),

                # Подсчет количества 2xx кодов
                func.count(case(
                    (Events.status_code.between(200, 299), 1),
                )).label('count_2xx'),

                # Подсчет количества 3xx кодов
                func.count(case(
                    (Events.status_code.between(300, 399), 1),
                )).label('count_3xx')

            ).filter(
                Events.response_time.between(response_time_1, response_time_2)
            ).group_by(
                Events.url_id
            )
        # Сортировка результатов
        if sort:
            if sort.startswith('-'):
                sort_field = sort[1:]
                order = False
            else:
                sort_field = sort
                order = True

            if sort_field == "created":
                query = query.order_by(
                    func.max(Events.created)) if order else query.order_by(
                    func.min(Events.created))

            if sort_field == "response_size":
                query = query.order_by(
                    func.max(
                        Events.response_size)) if order else query.order_by(
                    func.min(Events.response_size))

            if sort_field == "status_code":
                query = query.order_by(
                    func.max(
                        Events.status_code)) if order else query.order_by(
                    func.min(Events.status_code))

            if sort_field == "response_size":
                query = query.order_by(
                    func.max(
                        Events.response_size)) if order else query.order_by(
                    func.min(Events.response_size))

            result = query.all()

            list_events = [{"url_id": url[0], "avg_response_time": url[1],
                            "max_response_size": url[2],
                            "success_rate": (url[4] + url[5]) / url[3]} for
                           url in result]

            return jsonify(list_events)

    except SQLAlchemyError:
        raise HttpError(500, "Ошибка базы данных")

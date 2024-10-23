from celery import Celery
from celery.schedules import crontab
import time
import requests

from app.database import Session
from app.models.models import Url, Events
from flask import request, jsonify

celery_app = Celery('tasks', broker='redis://localhost:6379/0')



# def get_urls():
#     urls = request.session.query(Url).all()
#     for url in urls:
#         yield url
#
#
# def insert_records(records):
#     for event in records:
#         db_event = Events(
#             url_id=event["url_id"],
#             status_code=event["status_code"],
#             response_time=event["response_time"],
#             response_size=event["response_size"]
#         )
#         request.session.add(db_event)
#     request.session.commit()
#     return jsonify(records)
#
#
# @celery_app.task
# def main():
#     list_events = []
#     for url in get_urls():
#         url_path = url.path
#         start_time = time.time()
#
#         response = requests.get(url_path)
#
#         end_time = time.time()
#
#         status_code = response.status_code
#         url_id = url.id
#         response_time = end_time - start_time
#         response_size = len(response.content)
#
#         list_events.append({"url_id": url_id,
#                             "status_code": status_code,
#                             "response_time": response_time,
#                             "response_size": response_size})
#
#     insert_records(list_events)
#
#
# celery_app.conf.beat_schedule = {
#     'main': {
#         'task': "app.event.tasks.main",
#
#         'schedule': crontab(minute='*/1'),  # Запуск каждые 1 минуту
#     },
# }
@celery_app.task
def main(urls):
    list_events = []
    for url in urls:
        url_path = url['path']
        start_time = time.time()
        response = requests.get(url_path)
        end_time = time.time()

        status_code = response.status_code
        url_id = url['id']  # Используем словарь
        response_time = end_time - start_time
        response_size = len(response.content)

        list_events.append({
            "url_id": url_id,
            "status_code": status_code,
            "response_time": response_time,
            "response_size": response_size
        })

    insert_records(list_events)

def get_urls():
    session = Session()
    try:
        return session.query(Url).all()
    finally:
        session.close()

def insert_records(records):
    session = Session()
    try:
        for event in records:
            db_event = Events(
                url_id=event["url_id"],
                status_code=event["status_code"],
                response_time=event["response_time"],
                response_size=event["response_size"]
            )
            session.add(db_event)
        session.commit()
    finally:
        session.close()

@celery_app.task
def fetch_and_run():
    urls = get_urls()  # Получите URL без контекста запроса
    # Преобразуйте объекты Url в сериализуемый формат (список словарей)
    serialized_urls = [{'id': url.id, 'path': url.path} for url in urls]
    main.delay(serialized_urls)  # Передайте сериализованные URL в задачу main

celery_app.conf.beat_schedule = {
    'fetch_and_run': {
        'task': 'app.event.tasks.fetch_and_run',
        'schedule': crontab(minute='*/5'),
    },
}
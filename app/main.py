import time
import requests

from flask import request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Импортируем базы данных и модели
from app.database import Session, get_db
from app.event.views import get_events
from app.models.models import Url, Events, User

# Импортируем приложение и задачи
from app.apps import app
from app.event.tasks import main

# Импортируем представления
from app.url.views import get_url, add_url, remove_url
from app.user.views import add_user

# Импортируем админку
from app.user.admin import setup_admin

setup_admin(app)


# открываем сессию
@app.before_request
def before_request():
    session = Session()
    request.session = session


# закрываем сессию
@app.after_request
def after_request(response):
    request.session.close()
    return response


app.add_url_rule("/users", view_func=add_user, methods=["POST"])
app.add_url_rule("/urls", view_func=get_url, methods=["GET"],
                 endpoint='get_url')
app.add_url_rule("/urls", view_func=add_url, methods=["POST"],
                 endpoint='add_url')
app.add_url_rule("/urls/<string:url_id>", view_func=remove_url,
                 methods=["DELETE"], endpoint='remove_url')

app.add_url_rule("/events/<string:url_id>", view_func=get_events,
                 methods=["GET"], endpoint='get_events')


if __name__ == '__main__':
    app.run()

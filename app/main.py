from flask import request

from app.database import Session
from app.event.views import get_events, monitoring_statistics

from app.apps import app

from app.url.views import get_url, add_url, remove_url
from app.user.views import add_user

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

app.add_url_rule("/statistic", view_func=monitoring_statistics,
                 methods=["GET"], endpoint='monitoring_statistics')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()

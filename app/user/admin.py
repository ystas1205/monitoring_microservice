from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from app.database import Session
from app.models.models import User


def setup_admin(app):
    admin = Admin(app, name='MyApp Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, session=Session()))

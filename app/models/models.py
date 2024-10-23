from sqlalchemy import Column, Integer, String, \
    MetaData, func, UUID, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(UUID, server_default=func.gen_random_uuid(), unique=True)
    date_of_creation = Column(DateTime, default=func.current_timestamp())
    login = Column(String(50), nullable=False)

    urls = relationship("Url", backref="user")

    @property
    def dict(self):
        return {
            "id": self.id,
            "token": str(self.token),  # Преобразуем UUID в строку
            "date_of_creation": self.date_of_creation,
            "login": self.login
        }


class Url(Base):
    __tablename__ = "urls"

    id = Column(UUID, primary_key=True, server_default=func.gen_random_uuid(),
                unique=True)
    path = Column(String(300), nullable=False)
    date_of_creation = Column(DateTime, default=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))

    events = relationship("Events", backref="url")

    @property
    def dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "date_of_creation": self.date_of_creation,
            "user_id": self.user_id
        }


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(Integer, nullable=False)
    url_id = Column(UUID, ForeignKey("urls.id"))
    response_time = Column(Float, nullable=False)
    created = Column(DateTime, default=func.current_timestamp())
    response_size = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    @property
    def dict(self):
        return {
            "id": self.id,
            "status_code": self.status_code,
            "url_id": self.url_id,
            "response_time": self.response_time,
            "created": self.created,
            "response_size": self.response_size,
            "active": self.active
        }

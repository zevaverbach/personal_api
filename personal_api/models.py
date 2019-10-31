"""
BaseMixIn include `id` as the primary key,
as well as adding a self.when value in the constructor
"""
import datetime as dt
from sqlalchemy import Column, DateTime, String, Boolean, Date

from personal_api.database import Base, SessionLocal
from helpers import parse_date_string, BaseMixIn


def update(instance, **kwargs):
    for key, value in kwargs.items():
        setattr(instance, key, value)
    instance.when = dt.datetime.now()
    db = SessionLocal()
    db.commit()


class Resume(BaseMixIn, Base):
    __tablename__ = "résumé"

    when = Column(DateTime, nullable=False)
    url = Column(String, nullable=False, unique=True)


class Availability(BaseMixIn, Base):
    __tablename__ = "availability"

    when = Column(DateTime, nullable=False)
    available = Column(Boolean, nullable=False)
    next_available = Column(Date)

    def __init__(self, next_available=None, **kwargs):
        super().__init__(**kwargs)
        if next_available:
            self.next_available = parse_date_string(next_available)
        else:
            self.next_available = next_available


class Project(BaseMixIn, Base):
    # TODO: add 'tags' table and make a many-to-many relationship between projects and tags

    __tablename__ = 'projects'

    when = Column(DateTime, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    link = Column(String, unique=True)

    def update(self, **kwargs):
        update(self, **kwargs)

    def to_dict(self):
        return {attr_name: getattr(self, attr_name) for attr_name in ['title', 'description', 'link']}


class Post(BaseMixIn, Base):

    __tablename__ = "posts"

    when = Column(DateTime, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    body = Column(String, nullable=False)
    custom_url = Column(String)
    syndicate = Column(Boolean)

    def update(self, **kwargs):
        update(self, **kwargs)

    def to_dict(self):
        return {attr_name: getattr(self, attr_name)
                for attr_name in ['title', 'description', 'body', 'custom_url', 'syndicate']}

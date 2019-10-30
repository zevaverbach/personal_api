import datetime as dt

import dateparser as dp
from sqlalchemy import Column, Integer, desc

from app.database import SessionLocal


class Invalid(Exception):
    pass


def parse_date_string(date_string) -> dt.date:
    try:
        return dp.parse(date_string).date()
    except Exception:
        raise Invalid


class BaseMixIn:

    id = Column(Integer, primary_key=True, index=True)

    __mapper_args__ = {"order_by": desc("id")}

    def __init__(self, **kwargs):
        super(BaseMixIn, self).__init__(**kwargs)
        self.when = dt.datetime.now()

    @classmethod
    def delete_most_recent(cls):
        db = SessionLocal()
        db.delete(db.query(cls).first())
        db.commit()
from pydantic import BaseModel
from sqlalchemy.orm import Session

import app.models
from app.database import Base
from . import schemas


class DoesntExist(Exception):
    pass


class ArgumentError(Exception):
    pass


def create_thing(session: Session, model: Base, data: BaseModel):
    instance = model(**data.dict())
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def get_thing(session: Session, model: Base, thing_id: int = None, multi=False, **kwargs):
    if thing_id and multi:
        raise ArgumentError

    if thing_id:
        return session.query(model).filter_by(id=thing_id).first()
    elif kwargs:
        return session.query(model).filter_by(**kwargs).first()
    else:
        if multi:
            return session.query(model).all()
        else:
            return session.query(model).first()


def update_thing(db: Session,
                 model: Base,
                 schema: BaseModel,
                 thing_id: int,
                 **kwargs
                 ) -> BaseModel:
    if not kwargs:
        raise ArgumentError

    if any(kwarg_key not in schema.__fields__.keys() for kwarg_key in kwargs):
        raise ArgumentError

    thing = get_thing(db, model, thing_id=thing_id)
    if thing is None:
        raise DoesntExist

    for key, value in kwargs.items():
        setattr(thing, key, value)

    db.commit()
    db.refresh(thing)
    return schema(**thing.to_dict())


def delete_thing(db: Session,
                 model: Base,
                 thing_id: int):
    thing = get_thing(db, model=model, thing_id=thing_id)
    if not thing:
        raise DoesntExist
    else:
        db.delete(thing)
        db.commit()

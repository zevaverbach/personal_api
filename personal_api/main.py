from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from config import PERSONAL_API_USERNAME, PERSONAL_API_PASS
from personal_api import schemas, models
from .crud import (
    create_thing as create, get_thing as get, update_thing as update, DoesntExist,
    delete_thing as delete,
)
from .database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
security = HTTPBasic()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        # noinspection PyUnboundLocalVariable
        db.close()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != PERSONAL_API_USERNAME or credentials.password != PERSONAL_API_PASS:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Forbidden",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_root(_: str = Depends(get_current_username)):
    return {"Hello": "World"}


@app.get("/availability/", response_model=schemas.Availability)
def get_availability(db: Session = Depends(get_db), _: str = Depends(get_current_username)):
    return get(db, models.Availability)


@app.get("/resume/", response_model=schemas.Resume)
def get_resume(db: Session = Depends(get_db), _: str = Depends(get_current_username)):
    return get(db, models.Resume)


@app.get("/projects/", response_model=List[schemas.Project])
def get_projects(db: Session = Depends(get_db), _: str = Depends(get_current_username)):
    return get(db, models.Project, multi=True)


@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_projects(project_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_username)):
    return get(db, models.Project, thing_id=project_id)


@app.get("/posts/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), _: str = Depends(get_current_username)):
    return get(db, models.Post, multi=True)


@app.get("/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_username)):
    return get(db, models.Post, post_id)


@app.post("/posts/", response_model=schemas.Post)
def post_post(
        post_: schemas.PostCreate,
        db: Session = Depends(get_db),
        _: str = Depends(get_current_username)
):
    if get(db, model=models.Post, title=post_.title):
        raise HTTPException(status_code=409)
    return create(db, model=models.Post, data=post_)


@app.patch("/posts/{post_id}")
async def patch_project(post_id: int,
                        request: Request,
                        db: Session = Depends(get_db),
                        _: str = Depends(get_current_username),
                        ):
    return update(db, model=models.Post, schema=schemas.PostCreate, thing_id=post_id, **await request.json())


@app.post("/availability/", response_model=schemas.Availability)
def post_availability(
        availability: schemas.AvailabilityCreate,
        db: Session = Depends(get_db),
        _: str = Depends(get_current_username)
):
    return create(db, model=models.Availability, data=availability)


@app.post("/resume/", response_model=schemas.Resume)
def post_resume(
        resume: schemas.ResumeCreate,
        db: Session = Depends(get_db),
        _: str = Depends(get_current_username)
):
    return create(db, model=models.Resume, data=resume)


@app.post("/projects/", response_model=schemas.Project)
def post_project(
        project: schemas.ProjectCreate,
        db: Session = Depends(get_db),
        _: str = Depends(get_current_username)
):
    if get(db, model=models.Project, title=project.title):
        raise HTTPException(status_code=409)
    return create(db, model=models.Project, data=project)


@app.patch("/projects/{project_id}")
async def patch_project(project_id: int,
                        request: Request,
                        db: Session = Depends(get_db),
                        _: str = Depends(get_current_username),
                        ):
    return update(db, models.Project, schemas.ProjectCreate, project_id, **await request.json())


@app.delete("/projects/{project_id}")
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   _: str = Depends(get_current_username),
                   ):
    try:
        delete(db, models.Project, project_id)
    except DoesntExist:
        raise HTTPException(status_code=404)


@app.delete("/posts/{post_id}")
def delete_project(post_id: int,
                   db: Session = Depends(get_db),
                   _: str = Depends(get_current_username),
                   ):
    try:
        delete(db, models.Post, post_id)
    except DoesntExist:
        raise HTTPException(status_code=404)

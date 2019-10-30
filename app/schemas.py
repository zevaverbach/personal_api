from datetime import date, datetime

from pydantic import BaseModel, UrlStr


class AvailabilityBase(BaseModel):
    available: bool
    next_available: str = None


class AvailabilityCreate(AvailabilityBase):
    pass


class Availability(AvailabilityBase):
    id: int
    when: datetime
    next_available: date = None

    class Config:
        orm_mode = True


class ResumeBase(BaseModel):
    url: UrlStr


class ResumeCreate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int
    when: datetime

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    title: str
    description: str
    link: UrlStr = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    when: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: str
    body: str
    custom_url: str = None
    syndicate: bool = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    when: datetime

    class Config:
        orm_mode = True

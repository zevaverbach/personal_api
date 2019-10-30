# Personal API

Make a secured web API that stores and serves up your data!
The current schema is oriented towards powering freelancers' websites.

## Installation

Fork the project, then do `pipenv install`.

Set three config vars in your `.bashrc` etc.:

```
PERSONAL_API_USERNAME
PERSONAL_API_PASS
PERSONAL_API_SQLALCHEMY_DATABASE_URL
```

`PERSONAL_API_SQLALCHEMY_DATABASE_URL` should be for a postgres instance somewhere, in the format

`postgresql://{username}:{password}@{host}:{port}/{db_name}`

## Using Locally

Start the server with `uvicorn app.main:app`, then create, get, delete, and update records at will.

## Deployment

See "Using Locally", but point it at whatever web server you're using.

## Tables

As of today the available endpoints are

```
/availability
    id: int
    when: datetime
    available: bool
    next_available: datetime

    methods are GET and POST

/resume (versioned)
    id: int
    when: datetime
    url: str

    methods are GET and POST

/posts
    id: int
    when: datetime
    title: str
    description: str
    body: str
    custom_url: str (optional)
    syndicate: bool (optional)

    methods are GET, POST, PATCH, and DELETE

/projects
    id: int
    when: datetime
    title: str
    description: str
    link: str (optional)
```

## Dependencies

This project relies on the excellent work of 
[SQLALchemy](https://www.sqlalchemy.org/), 
[Pydantic](https://github.com/samuelcolvin/pydantic/),
[FastAPI](https://fastapi.tiangolo.com/),
[Pytest](https://docs.pytest.org/en/latest/contents.html),
and [Starlette](https://www.starlette.io/)

## Why?

It started as an excuse to get acquainted with FastAPI, as well as to make a front-end first (JAMstack?) personal site.

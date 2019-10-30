# Personal API

Make a secured web API that stores and serves up your own personal and professional data!
As of the current commit, it's oriented towards powering freelancers' websites.

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
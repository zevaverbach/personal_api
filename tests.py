"""
TODO: set up a test db or mocks instead of relying there being at least one item available in most of the 'get' tests.
"""
from starlette.testclient import TestClient

from config import PERSONAL_API_USERNAME, PERSONAL_API_PASS
from personal_api.main import app
from personal_api.models import Resume, Availability, Project, Post

client = TestClient(app)
VALID_AUTH = (PERSONAL_API_USERNAME, PERSONAL_API_PASS)


def test_main_no_auth():
    response = client.get('/')
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_main_wrong_auth():
    response = client.get('/', auth=('wronguser', 'wrongpass'))
    assert response.status_code == 401
    assert response.json() == {"detail": "Forbidden"}


def test_main_correct_auth():
    response = client.get('/', auth=VALID_AUTH)
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_get_availability():
    response = client.get('/availability/', auth=VALID_AUTH)
    assert response.status_code == 200


def test_set_availability():
    response = client.post('/availability/',
                           auth=VALID_AUTH,
                           json={
                               "available": False,
                               "next_available": "in two weeks",
                           })
    assert response.status_code == 200
    Availability.delete_most_recent()
    assert response.json()['available'] is False


def test_get_resume():
    response = client.get('/resume/', auth=VALID_AUTH)
    assert response.status_code == 200


def test_post_resume():
    response = client.post('/resume/', auth=VALID_AUTH, json={"url": "http://hypo.thetical"})
    assert response.status_code == 200
    Resume.delete_most_recent()
    assert response.json()['url'] == 'http://hypo.thetical'


def test_get_projects():
    response = client.get('/projects/', auth=VALID_AUTH)
    assert response.status_code == 200


def test_get_project():
    response = client.get('/projects/1', auth=VALID_AUTH)
    assert response.status_code == 200


def test_post_project():
    response = client.post('/projects/', auth=VALID_AUTH,
                           json={
                               "title": "Project Time",
                               "description": "This is a project I built one time.",
                               "link": "http://hypo.thetical",
                           })
    assert response.status_code == 200
    Project.delete_most_recent()
    assert response.json()['link'] == 'http://hypo.thetical'


def test_post_project_duplicate_title():
    projects = client.get('/projects/', auth=VALID_AUTH).json()
    existing_project = projects[0]
    original_title = existing_project['title']

    response = client.post('/projects/', auth=VALID_AUTH,
                           json={
                               "title": original_title,
                               "description": "yup"
                           })
    assert response.status_code == 409


def test_patch_project():
    projects = client.get('/projects/', auth=VALID_AUTH).json()
    existing_project = projects[0]
    original_title = existing_project['title']
    id_ = existing_project['id']

    response = client.patch(f'/projects/{id_}', auth=VALID_AUTH, json={"title": "Different Title"})
    assert response.status_code == 200
    new_title = response.json()['title']
    # put it back to how it was
    response = client.patch(f'/projects/{id_}', auth=VALID_AUTH, json={"title": original_title})
    assert response.status_code == 200
    assert new_title == "Different Title"


def test_get_posts():
    response = client.get('/posts/', auth=VALID_AUTH)
    assert response.status_code == 200


def test_post_post():
    response = client.post('/posts/', auth=VALID_AUTH,
                           json={
                               "title": "Project Time",
                               "body": "This is a project I built one time.",
                               "description": "yup"
                           })
    assert response.status_code == 200
    Post.delete_most_recent()
    assert response.json()['title'] == 'Project Time'


def test_post_post_insufficient_data():
    response = client.post('/posts/', auth=VALID_AUTH,
                           json={
                               "title": "Project Time",
                               "body": "This is a project I built one time.",
                           })
    assert response.status_code == 422


def test_post_post_duplicate_title():
    posts = client.get('/posts/', auth=VALID_AUTH).json()
    existing_post = posts[0]
    original_title = existing_post['title']

    response = client.post('/posts/', auth=VALID_AUTH,
                           json={
                               "title": original_title,
                               "body": "This is a project I built one time.",
                               "description": "yup"
                           })
    assert response.status_code == 409


def test_patch_post():
    posts = client.get('/posts/', auth=VALID_AUTH).json()
    existing_post = posts[0]
    original_title = existing_post['title']
    id_ = existing_post['id']

    response = client.patch(f'/posts/{id_}', auth=VALID_AUTH, json={"title": "Different Title"})
    assert response.status_code == 200
    new_title = response.json()['title']
    # put it back to how it was
    response = client.patch(f'/posts/{id_}', auth=VALID_AUTH, json={"title": original_title})
    assert response.status_code == 200
    assert new_title == "Different Title"


def test_delete_post():
    posts = client.get('/posts/', auth=VALID_AUTH).json()
    existing_post = posts[0]
    id_ = existing_post['id']
    response = client.delete(f"/posts/{id_}", auth=VALID_AUTH)
    assert response.status_code == 200

    # restore post
    response = client.post('/posts/', auth=VALID_AUTH,
                           json={
                               "title": existing_post['title'],
                               "body": existing_post['body'],
                               "description": existing_post['description'],
                           })
    assert response.status_code == 200


def test_delete_project():
    projects = client.get('/projects/', auth=VALID_AUTH).json()
    existing_project = projects[0]
    id_ = existing_project['id']
    print(id_)
    response = client.delete(f"/projects/{id_}", auth=VALID_AUTH)
    assert response.status_code == 200

    # restore project
    response = client.post('/projects/', auth=VALID_AUTH,
                           json={
                               "title": existing_project['title'],
                               "link": existing_project['link'],
                               "description": existing_project['description'],
                           })
    assert response.status_code == 200

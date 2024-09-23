import pytest
import sys
import os
from pprint import pprint as pp
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from app import create_app
from db import init_db, Admin, User, Class, Login, Logoff, generate_uid

def test_app_existence():
    assert create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_404(client):
    response = client.get("/asdsdgasad")
    assert b'404' in response.data

def test_index(client):
    response = client.get("/")
    assert b"Zeiterfassung by Saftladen GmbH" in response.data

def test_session(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["userid"] = 'JD0001010004'

    response = client.get("/", follow_redirects=True)
    assert response.request.path == '/user/JD0001010004'
    assert b'Einstempeln' in response.data and b'Ausstempeln' in response.data


def test_userpage_access_denied(client):
    get_response = client.get("/user/JD0001010004", follow_redirects=True)
    post_response = client.post("user/JD0001010004", data=
                                {
                                    "login": "time_in"
                                }, follow_redirects=True)
    assert post_response.request.path =='/'
    assert get_response.request.path == '/'

def test_userpage_access(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["userid"] = 'JD0001010004'

    get_response = client.get("/user/JD0001010004", follow_redirects=True)
    post_response = client.post("user/JD0001010004", data=
                                {
                                    "login": "time_in"
                                }, follow_redirects=True)
    assert post_response.status_code == 200
    assert post_response.request.path == '/user/JD0001010004'
    assert get_response.request.path == '/user/JD0001010004'
    assert b'Einstempeln' in get_response.data and b'Ausstempeln' in get_response.data

def test_userdashboard_access_denied(client):
    get_response = client.get("/user/JD0001010004/dashboard", follow_redirects=True)
    assert get_response.request.path == '/'

def test_userdashboard_access(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["userid"] = 'JD0001010004'

    get_response = client.get("/user/JD0001010004/dashboard", follow_redirects=True)
    assert get_response.request.path == '/user/JD0001010004/dashboard'
    assert b'Informationen' in get_response.data

def test_admin_access_denied(client):
    get_response = client.get("/admin/master", follow_redirects=True)
    post_response_user = client.post("/admin/master", data=
                                {
                                    'btn_add_user': 'adding_user'
                                }, follow_redirects=True)
    post_response_class = client.post("/admin/master", data=
                                {
                                    'btn_add_class': 'adding_class'
                                }, follow_redirects=True)
    assert post_response_user.request.path =='/'
    assert post_response_class.request.path =='/'
    assert get_response.request.path == '/'

def test_admin_adduser_access_denied(client):
    get_response = client.get("/admin/master/add_user", follow_redirects=True)
    post_response = client.post("/admin/master/add_user", data=
                                {
                                    'Name': 'Test',
                                    'Firstname': 'TestFirst',
                                    'DOB': '2000-01-01',
                                    'class_in': 'Testclass'
                                }, follow_redirects=True)
    assert post_response.request.path == '/'
    assert get_response.request.path == '/'

def test_admin_addclass_access_denied(client):
    get_response = client.get("/admin/master/add_user", follow_redirects=True)
    post_response = client.post("/admin/master/add_user", data=
                                {
                                    'CA': 'Test',
                                    'Subject_area': 'TestFirst',
                                    'Classroom': 'Testroom',
                                }, follow_redirects=True)
    assert post_response.request.path == '/'
    assert get_response.request.path == '/'
import pytest
import sys
import os
from pprint import pprint as pp
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from app import create_app

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

def test_userpage_access_denied(client):
    response = client.get("/user/JD0001010004", follow_redirects=True)
    assert response.request.path == '/'

def test_userdashboard_access_denied(client):
    response = client.get("/user/JD0001010004/dashboard", follow_redirects=True)
    assert response.request.path == '/'

def test_admin_access_denied(client):
    response = client.get("/admin/master", follow_redirects=True)
    assert response.request.path == '/'

def test_admin_adduser_access_denied(client):
    response = client.get("/admin/master/add_user", follow_redirects=True)
    assert response.request.path == '/'

def test_admin_addclass_access_denied(client):
    response = client.get("/admin/master/add_user", follow_redirects=True)
    assert response.request.path == '/'
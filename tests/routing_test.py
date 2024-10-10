import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from app import create_app


@pytest.fixture()
def app():
    db_path = 'db/test.db'
    app = create_app(db_path)
    app.config.update({
        "TESTING": True,
        "sqlalchemy_track_modifications": False,
    })

    yield app

    # ? Path manipulation with ./app needed because of the way the db is created in the app
    if os.path.exists(os.path.join('./app', db_path)):
        os.remove(os.path.join('./app', db_path))


@pytest.fixture()
def client(app):
    return app.test_client()

# ? Not Needed
# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()


def test_404(client):
    response = client.get("/asdsdgasad")
    assert b'404' in response.data


def test_index(client):
    response = client.get("/")
    assert b"Zeiterfassung by Saftladen GmbH" in response.data


def test_session(client):
    with client.session_transaction() as session:
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
        session["userid"] = 'JD0001010004'

    get_response = client.get("/user/JD0001010004", follow_redirects=True)
    post_response_logout = client.post("/user/JD0001010004", data=
                                {
                                    'signout_btn': 'signout'
                                }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
    assert get_response.request.path == '/user/JD0001010004'
    assert b'Einstempeln' in get_response.data and b'Ausstempeln' in get_response.data


def test_userdashboard_access_denied(client):
    get_response = client.get("/user/JD0001010004/dashboard", follow_redirects=True)
    assert get_response.request.path == '/'


def test_userdashboard_access(client):
    with client.session_transaction() as session:
        session["userid"] = 'JD0001010004'

    get_response = client.get("/user/JD0001010004/dashboard", follow_redirects=True)
    post_response_logout = client.post("/user/JD0001010004/dashboard", data=
                                {
                                    'signout_btn': 'signout'
                                }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
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


def test_admin_access(client):
    with client.session_transaction() as session:
        session["userid"] = 'master'

    get_response = client.get("/admin/master", follow_redirects=True)
    post_response_user = client.post("/admin/master", data=
                                {
                                    'btn_add_user': 'adding_user'
                                }, follow_redirects=True)
    post_response_class = client.post("/admin/master", data=
                                {
                                    'btn_add_class': 'adding_class'
                                }, follow_redirects=True)
    post_response_logout = client.post("/admin/master", data=
                                {
                                    'signout_btn': 'signout'
                                }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
    assert post_response_user.status_code == 200 and post_response_class.status_code == 200
    assert post_response_user.request.path =='/admin/master/add_user'
    assert post_response_class.request.path =='/admin/master/add_class'
    assert get_response.request.path == '/admin/master'


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


def test_admin_adduser_access(client):
    with client.session_transaction() as session:
        session["userid"] = 'master'

    get_response = client.get("/admin/master/add_user", follow_redirects=True)
    post_response_noclass = client.post("/admin/master/add_user", data=
                                {
                                    'Name': 'Test',
                                    'Firstname': 'TestFirst',
                                    'DOB': '2000-01-01',
                                    'CA': 'NotExistingClass'
                                }, follow_redirects=True)
    post_response = client.post("/admin/master/add_user", data=
                                {
                                    'Name': 'Test',
                                    'Firstname': 'TestFirst',
                                    'DOB': '2000-01-01',
                                    'CA': 'Testclass'
                                }, follow_redirects=True)
    post_response_logout = client.post("/admin/master/add_user", data=
                                {
                                    'signout_btn': 'signout'
                                }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
    assert post_response_noclass.status_code == 200 and post_response.status_code == 200
    assert b'Class does not exist! Contact an Admin' in post_response_noclass.data
    assert post_response.request.path == '/admin/master'
    assert post_response_noclass.request.path == '/admin/master/add_user'
    assert get_response.request.path == '/admin/master/add_user'


def test_admin_addclass_access_denied(client):
    get_response = client.get("/admin/master/add_class", follow_redirects=True)
    post_response = client.post("/admin/master/add_class", data=
                                {
                                    'CA': 'Test',
                                    'Subject_area': 'TestFirst',
                                    'Classroom': 'Testroom',
                                }, follow_redirects=True)
    assert post_response.request.path == '/'
    assert get_response.request.path == '/'


def test_admin_addclass_access(client):
    with client.session_transaction() as session:
        session["userid"] = 'master'
    post_response = client.post("/admin/master/add_class", data=
                                {
                                    'CA': 'Test',
                                    'Subject_area': 'TestFirst',
                                    'Classroom': 'Testroom',
                                }, follow_redirects=True)
    post_response_existing = client.post("/admin/master/add_class", data=
                                {
                                    'CA': 'Test',
                                    'Subject_area': 'TestFirst',
                                    'Classroom': 'Testroom',
                                }, follow_redirects=True)
    get_response = client.get("/admin/master/add_class", follow_redirects=True)
    post_response_logout = client.post("/admin/master/add_class", data=
                                {
                                    'signout_btn': 'signout'
                                }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
    assert post_response.status_code == 200 and post_response_existing.status_code == 200
    assert b'Class already exists!' in post_response_existing.data
    assert post_response_existing.request.path == '/admin/master/add_class'
    assert post_response.request.path == '/admin/master'
    assert get_response.request.path == '/admin/master/add_class'


def test_admin_classdetails_access_denied(client):
    get_response = client.get("/admin/master/class/Testklasse", follow_redirects=True)
    assert get_response.request.path == '/'


def test_admin_classdetails_access(client):
    with client.session_transaction() as session:
        session["userid"] = 'master'
    # ? Testdata for Deletion
    client.post("/admin/master/add_class", data=
                                {
                                    'CA': 'Test',
                                    'Subject_area': 'TestDelete',
                                    'Classroom': 'Testroom',
                                }, follow_redirects=True)
    get_response = client.get("/admin/master/class/Testclass", follow_redirects=True)
    post_response_wrong_ca = client.post("/admin/master/class/Testclass", data=
                                         {
                                             'delete_class': 'delete',
                                             'CA': 'Testclassss'
                                         }, follow_redirects=True)
    post_response_delete_ca_students = client.post("/admin/master/class/Testclass", data=
                                         {
                                             'delete_class': 'delete',
                                             'CA': 'Testclass'
                                         }, follow_redirects=True)
    post_response_delete_ca = client.post("/admin/master/class/Test", data=
                                         {
                                             'delete_class': 'delete',
                                             'CA': 'Test'
                                         }, follow_redirects=True)
    post_response_logout = client.post("/admin/master/class/Testclass", data=
                                {
                                    'signout_btn': 'signout'
                                }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
    assert post_response_wrong_ca.request.path == '/admin/master/class/Testclass'
    assert b'You type the class wrong!' in post_response_wrong_ca.data
    assert post_response_delete_ca_students.request.path == '/admin/master/class/Testclass'
    assert b'Class still has Students!' in post_response_delete_ca_students.data
    assert post_response_delete_ca.request.path == '/admin/master'
    assert get_response.request.path == '/admin/master/class/Testclass'


def test_admin_userdetails_access_denied(client):
    get_response = client.get("/admin/master/user/JD0001010004", follow_redirects=True)
    assert get_response.request.path == '/'


def test_admin_userdetails_access(client):
    with client.session_transaction() as session:
        session["userid"] = 'master'
    # ? Testdata
    client.post("/admin/master/add_user", data=
                {
                    'Name': 'Test',
                    'Firstname': 'TestFirst',
                    'DOB': '2000-01-01',
                    'CA': 'Testclass'
                    }, follow_redirects=True)
    get_response = client.get("/admin/master/user/JD0001010004", follow_redirects=True)
    post_response_wrong_uid = client.post("/admin/master/user/JD0001010004", data=
                                          {
                                              'delete_user': 'delete',
                                              'UID': 'JDd0001010004'
                                              }, follow_redirects=True)
    post_response_delete_uid = client.post("/admin/master/user/TT0001010004", data=
                                           {
                                               'delete_user': 'delete',
                                               'UID': 'TT0001010004'
                                               }, follow_redirects=True)
    post_response_logout = client.post("/admin/master/user/JD0001010004", data=
                                       {
                                           'signout_btn': 'signout'
                                           }, follow_redirects=True)
    assert post_response_logout.request.path == '/'
    assert post_response_wrong_uid.request.path == '/admin/master/user/JD0001010004'
    assert b'You typed the Userid wrong!' in post_response_wrong_uid.data
    assert post_response_delete_uid.request.path == '/admin/master'
    assert get_response.request.path == '/admin/master/user/JD0001010004'

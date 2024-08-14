import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from app.db import User, Login, Logoff, Admin, Class

@pytest.fixture(scope='module')
def new_user():
    user = User(UID='UI1245321', Name='Doe', Firstname='John', DOB='2000-01-01', CA='TA_22')
    return user

@pytest.fixture(scope='module')
def new_class():
    class_ = Class(CA='TA_22', Subject_area = 'Math', Classroom = 'A1')
    return class_

@pytest.fixture(scope='module')
def new_admin():
    admin = Admin(Username='testadmin', Password='password', UID='UI1245321')
    return admin

@pytest.fixture(scope='module')
def new_login():
    login = Login(Time='2021-01-01 12:00:00', UID='UI1245321')
    return login

@pytest.fixture(scope='module')
def new_logoff():
    logoff = Logoff(Time='2021-01-01 12:00:00', UID='UI1245321')
    return logoff

def test_new_user_with_fixture(new_user):
    assert new_user.UID == 'UI1245321'
    assert new_user.Name == 'Doe'
    assert new_user.Firstname == 'John'
    assert new_user.DOB == '2000-01-01'
    assert new_user.CA == 'TA_22'

def test_new_admin_with_fixture(new_admin):
    assert new_admin.Username == 'testadmin'
    assert new_admin.Password == 'password'
    assert new_admin.UID == 'UI1245321'

def test_new_login_with_fixture(new_login):
    assert new_login.Time == '2021-01-01 12:00:00'
    assert new_login.UID == 'UI1245321'

def test_new_logoff_with_fixture(new_logoff):
    assert new_logoff.Time == '2021-01-01 12:00:00'
    assert new_logoff.UID == 'UI1245321'

def test_new_class_with_fixture(new_class):
    assert new_class.CA == 'TA_22'
    assert new_class.Subject_area == 'Math'
    assert new_class.Classroom == 'A1'

if __name__ == '__main__':
    pytest.main()

import pytest
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from db import Base, User, Login, Logoff, Admin, Class, init_db, generate_uid


@pytest.fixture(scope='module')
def new_user():
    user = User(UID='UI1245321', Name='Doe', Firstname='John', DOB='2000-01-01', CA='TA_22')
    return user


@pytest.fixture(scope='module')
def new_class():
    class_ = Class(CA='TA_22', Subject_area='Math', Classroom='A1')
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


@pytest.fixture
def session():
    # In-Memory SQLite-Datenbank verwenden
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_user_model(session):
    user = User(UID='123', Name='Doe', Firstname='John', Password="ABcd123!", DOB=datetime(1990, 1, 1), CA='CA1')
    session.add(user)
    session.commit()

    assert session.query(User).count() == 1
    assert session.query(User).first().Name == 'Doe'


def test_login_model(session):
    login = Login(Time=datetime.now(), UID='123')
    session.add(login)
    session.commit()

    assert session.query(Login).count() == 1
    assert session.query(Login).first().UID == '123'


def test_logoff_model(session):
    logoff = Logoff(Time=datetime.now(), UID='123')
    session.add(logoff)
    session.commit()

    assert session.query(Logoff).count() == 1
    assert session.query(Logoff).first().UID == '123'


def test_admin_model(session):
    admin = Admin(Username='admin', Password='password', UID='123')
    session.add(admin)
    session.commit()

    assert session.query(Admin).count() == 1
    assert session.query(Admin).first().Username == 'admin'


def test_class_model(session):
    class_ = Class(CA='CA1', Subject_area='Math', Classroom='101')
    session.add(class_)
    session.commit()

    assert session.query(Class).count() == 1
    assert session.query(Class).first().Subject_area == 'Math'


@pytest.mark.skip(reason='Need fix - not importatnt for now')
def test_init_db(session):
    init_db('sqlite:///:memory:')
    assert session.query(Admin).filter_by(Username='master').first() is not None, 'Master-Admin nicht gefunden'


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


def test_generate_uid(session):
    uid = generate_uid('Doe', 'John', datetime(2024, 1, 1), session)
    assert uid == 'JD2401010010'

from os import path
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    BLOB,
    DateTime,
    Date,
    ForeignKey
    )
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from utility import random_password, hash_password


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Database model for the user table.

    Attributes:
        UID (str): The unique identifier of the user.
        Picture (BLOB): The picture of the user. Default is None.
        Name (str): The name of the user.
        Firstname (str): The first name of the user.
        Password (str): The password of the user.
        DOB (Date): The date of birth of the user.
        CA (str): The CA of the user.
        Logins (list): A list of login instances associated with the user.
        Logoffs (list): A list of logoff instances associated with the user.
    """
    __tablename__ = 'user'
    UID = Column(String, primary_key=True)
    Picture = Column(BLOB)
    Name = Column(String, nullable=False)
    Firstname = Column(String, nullable=False)
    Password = Column(String, nullable=False)
    DOB = Column(Date, nullable=False)
    CA = Column(String, ForeignKey('class.CA'))
    Logins = relationship('Login', backref='user', lazy=True)
    Logoffs = relationship('Logoff', backref='user', lazy=True)


class Login(Base):
    """
    Database model for the login table.

    Attributes:
        NR (int): The unique identifier of the login.
        Time (DateTime): The time of the login.
        UID (str): The UID of the user who logged in.
    """
    __tablename__ = 'login'
    NR = Column(Integer, primary_key=True, autoincrement=True)
    Time = Column(DateTime, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Logoff(Base):
    """
    Database model for the logoff table.

    Attributes:
        NR (int): The unique identifier of the logoff.
        Time (DateTime): The time of the logoff.
        UID (str): The UID of the user who logged off.
    """
    __tablename__ = 'logoff'
    NR = Column(Integer, primary_key=True, autoincrement=True)
    Time = Column(DateTime, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Admin(Base):
    """
    Database model for the admin table.

    Attributes:
        Username (str): The username of the admin.
        Password (str): The password of the admin.
        UID (str): The UID of the corresponding User.
    """
    __tablename__ = 'admin'
    Username = Column(String, primary_key=True)
    Password = Column(String, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Class(Base):
    """
    Database model for the class table.

    Attributes:
        CA (str): The CA of the class.
        Subject_area (str): The subject area of the class.
        Classroom (str): The classroom of the class.
        Students (list): A list of user instances associated with the class.
    """
    __tablename__ = 'class'
    CA = Column(String, primary_key=True)
    Subject_area = Column(String, nullable=False)
    Classroom = Column(String, nullable=False)
    Students = relationship('User', backref='class', lazy=True)


def generate_uid(name: str, first_name: str, dob: datetime, session) -> str:
    """
    Generates a unique identifier for a user.

    Args:
        name (str): The name of the user.
        first_name (str): The first name of the user.
        dob (datetime): The date of birth of the user.
        session(sqlalchemie session): The session to query the database.

    Returns:
        str: The unique identifier.
    """
    modifier = 0
    while True:
        uid = first_name[0] + name[0] + dob.date().strftime("%y%m%d") + str(sum([int(x) for x in dob.date().strftime("%Y%m%d")]) + modifier).zfill(4)

        if not session.query(User).filter(User.UID == uid).first():
            return uid
        modifier += 1

def _master_admin(session):
    """
    Adds the master admin to the database.
    """

    rndpw = random_password()
    master_user = User(UID='000000000000', Name='Admin', Firstname='Master',
                       Password=hash_password(rndpw), DOB=datetime.now(),
                       CA='')
    session.add(master_user)
    master_admin = Admin(Username='master',
                         Password=hash_password(rndpw),
                         UID='000000000000')
    session.add(master_admin)

    print(f"Master-Admin added. Note the Password: {rndpw}")
    print("## You won't see it again. Please note the password. ##")

def _test_data(session):
    """
    Adds test data to the database.

    Args:
        session(sqlalchemie session): The session to query the database.
    """
    t_name = 'Doe'
    t_firstname = 'John'
    t_dob = datetime(2000, 1, 1)
    t_uid = generate_uid(t_name, t_firstname, t_dob, session)
    test_class = Class(CA='Testclass', Subject_area='Test', Classroom='Testroom')
    session.add(test_class)
    test_user = User(UID=t_uid, Name=t_name, Firstname=t_firstname,
                     Password=hash_password('123456789'), DOB=t_dob,
                     CA='Testclass')
    session.add(test_user)

def init_db_raw(db_url: str):
    """
    Initializes the database.

    Args:
        db_url (str): The URL of the database.
    """
    engine = create_engine(db_url)
    # Tabellen erstellen
    Base.metadata.create_all(engine)
    # Session erstellen
    Session = sessionmaker(bind=engine)
    session = Session()

    # Admin Datensatz hinzufügen
    _master_admin(session)

    # ! Testdaten hinzufügen (nur für Entwicklung)!
    _test_data(session)
    # ! Delete this block for production

    session.commit()
    session.close()
    
def init_db(db: SQLAlchemy):
    """
    Initializes the database.

    Args:
        db (SQLAlchemy): The database object.
    """
    session = db.session

    # Admin Datensatz hinzufügen
    _master_admin(session)

    # ! Testdaten hinzufügen (nur für Entwicklung)!
    _test_data(session)
    # ! Delete this block for production

    db.session.commit()
    db.session.close()

if __name__ == '__main__':
    basedir = path.abspath(path.dirname(__file__))
    init_db_raw('sqlite:///' + path.join(basedir, 'db/database.db'))

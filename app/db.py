from os import path
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey
    )
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from utility import random_password, hash_password

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    UID = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Firstname = Column(String, nullable=False)
    DOB = Column(Date, nullable=False)
    CA = Column(String, ForeignKey('class.CA'))
    Logins = relationship('Login', backref='user', lazy=True)
    Logoffs = relationship('Logoff', backref='user', lazy=True)


class Login(Base):
    __tablename__ = 'login'
    NR = Column(Integer, primary_key=True, autoincrement=True)
    Time = Column(DateTime, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Logoff(Base):
    __tablename__ = 'logoff'
    NR = Column(Integer, primary_key=True, autoincrement=True)
    Time = Column(DateTime, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Admin(Base):
    __tablename__ = 'admin'
    Username = Column(String, primary_key=True)
    Password = Column(String, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Class(Base):
    __tablename__ = 'class'
    CA = Column(String, primary_key=True)
    Subject_area = Column(String, nullable=False)
    Classroom = Column(String, nullable=False)
    Students = relationship('User', backref='class', lazy=True)


def init_db(db_url: str):
    engine = create_engine(db_url)
    # Tabellen erstellen
    Base.metadata.create_all(engine)
    # Session erstellen
    Session = sessionmaker(bind=engine)
    session = Session()

    # Beispiel-Datensatz hinzufügen
    rndpw = random_password()
    master_admin = Admin(Username='master', Password=hash_password(rndpw))
    session.add(master_admin)
    session.commit()
    print(f"Master-Admin added. Note the Password: {rndpw}")
    print("## You won't see it again. Please note the password. ##")


if __name__ == '__main__':
    basedir = path.abspath(path.dirname(__file__))
    init_db('sqlite:///' + path.join(basedir, 'db/database.db'))

import os
import random
import string
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

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
    master_admin = Admin(Username='master', Password=_generate_password())
    session.add(master_admin)
    session.commit()

def _generate_password():
    notallowed = '²³{[]}^`´'
    letters = string.digits + string.ascii_letters + string.punctuation
    
    for x in notallowed:
        letters = letters.replace(x, '')
    
    pw = ''.join(random.choice(letters) for i in range(10))
    return pw


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    init_db('sqlite:///' + os.path.join(basedir, 'db/database.db'))

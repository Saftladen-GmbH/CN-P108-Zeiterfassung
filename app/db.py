import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/database.db')
db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        with open('app/db/schema.sql', 'r') as file:
            sql_commands = file.read()
        with db.engine.connect() as connection:
            connection.execute(sql_commands)


if __name__ == '__main__':
    init_db()

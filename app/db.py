from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        with open('schema.sql', 'r') as file:
            sql_commands = file.read()
        db.engine.execute(sql_commands)


if __name__ == '__main__':
    init_db()

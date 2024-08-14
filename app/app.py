import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from db import init_db, Admin, User, Class, Login, Logoff

# Database initialization
basedir = os.path.abspath(os.path.dirname(__file__))
path2db = os.path.join(basedir, 'db/database.db')
sqpath = 'sqlite:///' + os.path.join(basedir, 'db/database.db')

if not os.path.exists(os.path.join(basedir, 'db/database.db')):
    print("Database not generated. Generating database")
    init_db(sqpath)

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = sqpath
db = SQLAlchemy(server)

@server.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    server.run("0.0.0.0", "5005", debug=True)

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/database.db')
db = SQLAlchemy(server)

@server.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    server.run("0.0.0.0", "5005", debug=True)

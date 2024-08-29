from os import path
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import init_db, Admin, User, Class, Login, Logoff
from utility import hash_password, verify_password

server = Flask(__name__)

# Database initialization
basedir = path.abspath(path.dirname(__file__))
path2db = path.join(basedir, 'db/database.db')
sqpath = 'sqlite:///' + path.join(basedir, 'db/database.db')

if not path.exists(path.join(basedir, 'db/database.db')):
    print("Database not generated. Generating database")
    init_db(sqpath)

# Database configuration
server.config['SQLALCHEMY_DATABASE_URI'] = sqpath
db = SQLAlchemy(server)


@server.route("/")
def index():
    return render_template("index.html")


# Remove second route and default value for production !!
@server.route("/user_JD0001010004", methods=["POST", "GET"])
@server.route("/user_<userid>", methods=["POST", "GET"])
def user(userid: str = 'JD0001010004'):
    """User Page to start logging Time

    Args:
        userid (str): Needs to be given to load User Data! Defaults to test for DEV

        !!REMOVE SECOND ROUTE AND DEFAULT VALUE FOR PRODUCTION!!

    Returns:
        Page: User Page
    """
    user_data = db.session.query(User).filter_by(UID=userid).first()
    if request.method == "POST":
        if request.form['login'] == 'time_in':
            new_login = Login(Time=datetime.now(), UID=userid)
            db.session.add(new_login)
            db.session.commit()
        return redirect(url_for("user", userid=userid))
    else:
        return render_template("user.html",
                            logins=user_data.Logins,
                            logouts=user_data.Logoffs,
                            user=user_data)


if __name__ == "__main__":
    server.run("0.0.0.0", "5005", debug=True)

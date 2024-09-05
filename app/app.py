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

if not path.exists(path2db):
    print("Database not generated. Generating database")
    init_db(sqpath)

# Database configuration
server.config['SQLALCHEMY_DATABASE_URI'] = sqpath
db = SQLAlchemy(server)


@server.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return redirect(url_for("user", userid=request.form.get("username")))
    else:
        return render_template("index.html")

# Remove second route and default value for production !!
@server.route("/user/JD0001010004/dashboard", methods=["POST", "GET"])
@server.route("/user/<userid>/dashboard", methods=["POST", "GET"])
def dashboard(userid: str = 'JD0001010004'):
    """Dashboard Page to display User Data

    Args:
        userid (str): Needs to be given to load User Data!
                      Defaults to testuser UID for DEV

        !!REMOVE SECOND ROUTE AND DEFAULT VALUE FOR PRODUCTION!!

    Returns:
        Page: Index Page
        Page: Not Found
        Page: Dashboard Page
    """
    # user_data = db.session.query(User).filter_by(UID=userid).first()
    user_data = db.get_or_404(User, userid)
    return render_template("user_dashboard.html", user=user_data)

# Remove second route and default value for production !!
@server.route("/user/<userid>/", methods=["POST", "GET"])
def user(userid: str):
    """User Page to start logging Time In and Time Out

    Args:
        userid (str): Needs to be given to load User Data!
                      Defaults to testuser UID for DEV

        !!REMOVE SECOND ROUTE AND DEFAULT VALUE FOR PRODUCTION!!

    Returns:
        Page: Index Page
        Page: Not Found
        Page: User Page
    """
    # user_data = db.session.query(User).filter_by(UID=userid).first()
    user_data = db.get_or_404(User, userid)
    state = ['', 'disabled']

    if len(user_data.Logins) > 0 and len(user_data.Logoffs) > 0:
        last_login = user_data.Logins[-1]
        last_logoff = user_data.Logoffs[-1]
        if last_login.Time < last_logoff.Time:
            state = ['', 'disabled']
        else:
            state = ['disabled', '']
    elif len(user_data.Logins) > 0:
        last_login = user_data.Logins[-1]
        state = ['disabled', '']
    else:
        last_login = []
        last_logoff = []

    if request.method == "POST":
        current_time = datetime.now()
        if request.form.get('login') == 'time_in':
            data = Login(Time=current_time, UID=userid)
        elif request.form.get('logout') == 'time_out':
            data = Logoff(Time=current_time, UID=userid)
        elif request.form.get('signout_btn') == 'signout':
            # !!!!
            # CODE TO SIGN OUT OF SESSION
            # !!!!
            return redirect(url_for("index"))
        db.session.add(data)
        db.session.commit()
        return redirect(url_for("user", userid=userid))
    else:
        return render_template("user.html",
                               logins=user_data.Logins,
                               logouts=user_data.Logoffs,
                               user=user_data,
                               in_state=state[0],
                               out_state=state[1],)


if __name__ == "__main__":
    server.run("0.0.0.0", "5005", debug=True)

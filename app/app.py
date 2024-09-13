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


@server.route("/user/<userid>/dashboard", methods=["POST", "GET"])
def dashboard(userid):
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


    all_logins = user_data.Logins
    all_logins.sort(key=lambda x: x.Time, reverse=True)
    reduced_logins = all_logins[:9]

    # Das was wir gestern versucht habe, hat nicht geklappt weil:
    # Die daten die aus user_data.Logins kommen sind keine konventionellen DICTS
    # Sondern sind Objekte. Demnach können wir da nichts Anfügen. Mit der erstellung einer
    # "Hilfsliste" geht es jetzt. Bei frage frag.

    # Erstellt eine neue Liste wo auf dem Index 0 das Login Objekt ist
    # Auf index 1 dann der typ. Habe dir deinen Code schon angepasst. 
    combined_logins = [[x, "login"] for x in reduced_logins]

    all_logouts = user_data.Logoffs
    all_logouts.sort(key=lambda x: x.Time, reverse=True)
    reduced_logouts = all_logouts[:9]

    # Erstellt eine neue Liste wo auf dem Index 0 das Login Objekt ist
    # Auf index 1 dann der typ. Habe dir deinen Code schon angepasst. 
    combined_logouts = [[x, "logout"] for x in reduced_logouts]

    total_list = combined_logins + combined_logouts
    total_list.sort(key=lambda x: x[0].Time)
    return render_template("user_dashboard.html", user=user_data, all_logins=all_logins, all_logouts=all_logouts, total_list=total_list)

# Remove second route and default value for production !!
@server.route("/user/<userid>", methods=["POST", "GET"])
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

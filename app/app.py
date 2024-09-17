from os import path
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from db import init_db, Admin, User, Class, Login, Logoff
from utility import hash_password, verify_password, user_logout, verify_login

server = Flask(__name__)

server.secret_key = '1234566789'

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
        userid = request.form.get("username").upper()
        password = request.form.get("password")

        user_data = db.session.query(User).filter_by(UID=userid).first()
        admin_data = db.session.query(Admin).filter_by(Username=userid.lower()).first()

        if user_data:
            if verify_password(user_data.Password, password) and userid == user_data.UID:
                # Password and Username correct
                print("User Found and Password Correct! Redirect to Userpage")
                session["userid"] = userid
                return redirect(url_for("user", userid=userid))
            else:
                # Password incorrect
                print("Password Incorrect!")
                return render_template("index.html", error="Incorrect Password!")
        else:
            # try admin
            if admin_data:
                if verify_password(admin_data.Password, password) and userid.lower() == admin_data.Username:
                    # Password and Username correct
                    aid = userid.lower()
                    session["userid"] = aid
                    print("Admin Found and Password Correct! Redirect to Admindashboard")
                    return redirect(url_for("admin", AID=aid))
                else:
                    # Password incorrect
                    print("Password Incorrect!")
                    return render_template("index.html", error="Incorrect Password!")
            else:
                # User not found - Bad UserID ?
                print("User not found!")
                return render_template("index.html", error="User not found!")
    else:
        if session.get("userid") and db.session.get(User, session.get("userid")):
            return redirect(url_for("user", userid=session.get("userid")))
        elif session.get("userid") and db.session.get(Admin, session.get("userid")):
            return redirect(url_for("admin", AID=session.get("userid")))
        else:
            return render_template("index.html", error="")


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
    if not verify_login(session, userid):
        return redirect(url_for("index"))

    if request.method == "POST":
        if request.form.get('signout_btn') == 'signout':
            return user_logout(session)
    else:
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
        total_list.sort(key=lambda x: x[0].Time, reverse=True)
        return render_template("user_dashboard.html", user=user_data, all_logins=all_logins, all_logouts=all_logouts, total_list=total_list)


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
    if not verify_login(session, userid):
        return redirect(url_for("index"))

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
            return user_logout(session)
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


@server.route("/admin/<AID>/", methods=["POST", "GET"])
def admin(AID: str):
    """Admin Page to manage Users and Classes"""

    if not verify_login(session, AID):
        return redirect(url_for("index"))

    if request.method == "POST":
        if request.form.get('signout_btn') == 'signout':
            return user_logout(session)
    else:
        # ! Pages function not tested yet!
        page = request.args.get('page', 1, type=int)
        per_page = 20

        admin_data = db.get_or_404(Admin, AID)
        pagination = db.paginate(select=db.select(User), page=page, per_page=per_page, error_out=False)

        all_users = pagination.items
        return render_template("admin.html", data=admin_data, users=all_users, pagination=pagination)


@server.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    server.run("0.0.0.0", "5005", debug=True)

from os import path
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from db import init_db, Admin, User, Class, Login, Logoff, generate_uid
from utility import random_password, hash_password, verify_password, user_logout, verify_login, calculate_time_history

db = SQLAlchemy()


def create_app(db_path: str = 'db/database.db') -> Flask:
    server = Flask(__name__)

    server.secret_key = '1234566789'

    # Database initialization
    basedir = path.abspath(path.dirname(__file__))
    path2db = path.join(basedir, db_path)
    sqpath = 'sqlite:///' + path.join(basedir, db_path)

    if not path.exists(path2db):
        print("Database not generated. Generating database")
        init_db(sqpath)

    # Database configuration
    server.config['SQLALCHEMY_DATABASE_URI'] = sqpath
    db.init_app(app=server)

    @server.route("/", methods=["POST", "GET"])
    def index():
        if request.method == "POST":
            userid = request.form.get("username").replace(" ", "").upper()
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

            combined_logins = [[x, "login"] for x in reduced_logins]

            all_logouts = user_data.Logoffs
            all_logouts.sort(key=lambda x: x.Time, reverse=True)
            reduced_logouts = all_logouts[:9]

            combined_logouts = [[x, "logout"] for x in reduced_logouts]

            total_list = combined_logins + combined_logouts
            total_list.sort(key=lambda x: x[0].Time, reverse=True)
            time_history = {k: v.total_seconds() for k, v in calculate_time_history(total_list).items()}
            return render_template("user_dashboard.html", user=user_data, total_list=total_list, time_history=time_history, timedelta=timedelta)

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

    @server.route("/admin/<AID>", methods=["POST", "GET"])
    def admin(AID: str, **kwargs):
        """Admin Page to manage Users and Classes"""

        if not verify_login(session, AID):
            return redirect(url_for("index"))

        if request.method == "POST":
            if request.form.get('signout_btn') == 'signout':
                return user_logout(session)
            elif request.form.get('btn_add_user') == 'adding_user':
                return redirect(url_for("adduser", AID=session.get("userid")))
            elif request.form.get('btn_add_class') == 'adding_class':
                return redirect(url_for("addclass", AID=session.get("userid")))
        else:
            user_page = request.args.get('userpage', 1, type=int)
            class_page = request.args.get('classpage', 1, type=int)

            per_page_class = 10
            per_page_user = 10

            admin_data = db.get_or_404(Admin, AID)

            pagination_users = db.paginate(select=db.select(User), page=user_page, per_page=per_page_user, error_out=False)
            pagination_classes = db.paginate(select=db.select(Class), page=class_page, per_page=per_page_class, error_out=False)

            all_users = pagination_users.items
            all_classes = pagination_classes.items

            return render_template("admin.html", data=admin_data,
                                                user_pages={
                                                    'data': all_users,
                                                    'pagination': pagination_users
                                                    },
                                                class_pages={
                                                    'data': all_classes,
                                                    'pagination': pagination_classes
                                                })

    @server.route("/admin/<AID>/add_user", methods=["POST", "GET"])
    def adduser(AID):
        if not verify_login(session, AID):
            return redirect(url_for("index"))

        existing_classes = [row[0] for row in db.session.query(Class.CA).all()]

        if request.method == "POST":
            if request.form.get('signout_btn') == 'signout':
                return user_logout(session)
            name_in = request.form.get("Name")
            fistname_in = request.form.get("Firstname")
            dob_in = datetime.strptime(request.form.get("DOB"), "%Y-%m-%d")
            class_in = request.form.get("CA")

            if class_in not in existing_classes:
                return render_template("user_add.html",
                                       error="Class does not exist! Contact an Admin",
                                       existing_classes=existing_classes)

            uid_gen = generate_uid(name_in, fistname_in, dob_in, db.session)
            pw_gen = random_password()

            user_data = User(UID=uid_gen,
                             Name=name_in,
                             Firstname=fistname_in,
                             Password=hash_password(pw_gen),
                             DOB=dob_in,
                             CA=class_in)

            db.session.add(user_data)
            db.session.commit()

            flash(f"User added. Note the Password: '{pw_gen}' and give it to {user_data.Firstname} {user_data.Name}!")
            return redirect(url_for("admin", AID=session.get("userid")))

        return render_template("user_add.html",
                               AID=session.get('userid'),
                               error="",
                               existing_classes=existing_classes)

    @server.route("/admin/<AID>/add_class", methods=["POST", "GET"])
    def addclass(AID):
        if not verify_login(session, AID):
            return redirect(url_for("index"))

        existing_classes = [row[0] for row in db.session.query(Class.CA).all()]

        if request.method == "POST":
            if request.form.get('signout_btn') == 'signout':
                return user_logout(session)
            ca_in = request.form.get("CA")
            subject_area_in = request.form.get("Subject_area")
            classroom_in = request.form.get("Classroom")

            if ca_in in existing_classes:
                return render_template("class_add.html",
                                       AID=session.get('userid'),
                                       error="Class already exists!")

            class_data = Class(CA=ca_in,
                               Subject_area=subject_area_in,
                               Classroom=classroom_in)

            db.session.add(class_data)
            db.session.commit()

            flash(f"Class added: {ca_in}")

            return redirect(url_for("admin",
                                    AID=session.get("userid")))

        return render_template("class_add.html",
                               AID=session.get('userid'),
                               error="")

    @server.route("/admin/<AID>/user/<UID>", methods=["POST", "GET"])
    def admin_userdetails(AID, UID):
        if not verify_login(session, AID):
            return redirect(url_for("index"))
        user_data = db.get_or_404(User, UID)
        all_logins = user_data.Logins
        all_logins.sort(key=lambda x: x.Time, reverse=True)
        reduced_logins = all_logins[:9]

        combined_logins = [[x, "login"] for x in reduced_logins]
        all_logouts = user_data.Logoffs
        all_logouts.sort(key=lambda x: x.Time, reverse=True)
        reduced_logouts = all_logouts[:9]
        combined_logouts = [[x, "logout"] for x in reduced_logouts]

        total_list = combined_logins + combined_logouts
        total_list.sort(key=lambda x: x[0].Time, reverse=True)
        time_history = {k: v.total_seconds() for k, v in calculate_time_history(total_list).items()}
        return render_template("admin_userdetails.html", user=user_data, AID=AID, time_history=time_history, timedelta=timedelta)

    @server.route("/admin/<AID>/class/<CA>", methods=["POST", "GET"])
    def admin_classdetails(AID, CA):
        if not verify_login(session, AID):
            return redirect(url_for("index"))
        class_data = db.get_or_404(Class, CA)
        return render_template("admin_classdetails.html", class_data=class_data, AID=AID)

    @server.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return server


if __name__ == "__main__":
    app = create_app()
    app.run("0.0.0.0", "5005", debug=True)

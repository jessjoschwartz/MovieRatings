from flask import Flask, render_template, redirect, request, url_for, Blueprint
from flask.ext.login import login_required, login_user, logout_user

from flask_tracking.data import db
from .forms import LoginForm, RegistrationForm
from .models import User

import model
app = Flask(__name__)

users = Blueprint('users', __name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/show_users")
def show_all_users():
    user_list = model.session.query(model.User).limit(15).all()
    return render_template("show_all_users.html", user_list=user_list)

@app.route("/show_ratings")
def show_all_ratings():
    user_id = request.args.get("user_id")
    ratings = model.session.query(model.Rating).filter(model.Rating.user_id==user_id).limit(15).all()
    return render_template("show_all_ratings.html", ratings=ratings, user_id=user_id)

@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Let Flask-Login know that this user
        # has been authenticated and should be
        # associated with the current session.
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("tracking.index"))
    return render_template('users/login.html', form=form)

@users.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('tracking.index'))
    return render_template('users/register.html', form=form)


@users.route('/logout/')
@login_required
def logout():
    # Tell Flask-Login to destroy the
    # session->User connection for this session.
    logout_user()
    return redirect(url_for('tracking.index'))

# @app.route("/login", methods=["GET"])
# def show_login():
#     return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def process_login():
#     """TODO: Receive the user's login credentials located in the 'request.form'
#     dictionary, look up the user, and store them in the session."""

#     f = request.form

#     user_email = f.get('email')
#     customer = model.get_user_by_email(user_email)

#     if customer == None:
#         print "You're not in the database!"
#         flash("You're not in the database!")
#     else:
#         session['name'] = customer.firstname
#         flash("You've successfully logged on! Yay!")


#     return redirect("/melons")

if __name__ == "__main__":
    app.run(debug = True)

    
    # model.session.query(model.Rating).filter(id=user.id).all()
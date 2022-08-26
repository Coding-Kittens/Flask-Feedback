from flask import Flask, render_template, redirect, session, flash
from models import *
from forms import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "catsarethebest"

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """Redirects to /register if not logged in"""
    if "username" in session:
        username = session["username"]
        return redirect(f"/users/{username}")
    return redirect("/register")


@app.route("/register", methods=["GET"])
def show_register_form():
    """Shows the Sign Up form"""
    form = SignUpForm()
    return render_template("sign_up_form.html", form=form)


@app.route("/register", methods=["POST"])
def register_user():
    """Makes a new user"""
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            new_user = User.register(
                form.username.data,
                form.password.data,
                form.email.data,
                form.first_name.data,
                form.last_name.data,
            )
            session["username"] = new_user.username
            db.session.add(new_user)
            db.session.commit()
            flash(f"Welcome {new_user.username}!")
            return redirect(f"/users/{new_user.username}")
        except:
            flash("Username is already taken, please pick a different one.")

    return redirect("/register")


@app.route("/login", methods=["GET"])
def show_login_form():
    """Shows the login form"""
    form = LoginForm()
    return render_template("login_form.html", form=form)


@app.route("/login", methods=["POST"])
def login_user():
    """Process the login form. if the user is authenticated goes to /users/<username>"""
    form = LoginForm()
    if form.validate_on_submit():
        current_user = User.authenticate(form.username.data, form.password.data)
        if current_user:
            session["username"] = current_user.username
            flash(f"Welcome back {current_user.username}!", "info")
            return redirect(f"/users/{current_user.username}")
        else:
            form.username.errors = ["Invalid username or password, please try again."]

    return redirect("/login")


@app.route("/users/<username>", methods=["GET"])
def secret_page(username):
    """Shows the user page to loged in users"""
    if "username" in session and session["username"] == username:
        current_user = User.query.get_or_404(username)
        return render_template("user.html", current_user=current_user)
    flash("Please login to view this page!")
    return redirect("/login")


@app.route("/logout", methods=["GET"])
def logout_user():
    """Logs out current user"""
    session.pop("username")
    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes user"""
    if "username" in session and session["username"] == username:
        current_user = User.query.get_or_404(username)
        session.pop("username")
        current_user.feedback = []
        User.query.filter_by(username=username).delete()
        db.session.commit()
        flash("Deleted User")
    return redirect("/register")


@app.route("/users/<username>/feedback/add", methods=["GET"])
def show_add_feedback(username):
    """Shows add feedback form"""
    if "username" in session and session["username"] == username:
        form = FeedbackForm()
        return render_template("add_feedback_form.html", form=form)
    flash("Please login to add feedback!")
    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["POST"])
def add_feedback(username):
    """Adds feedback"""
    if "username" in session and session["username"] == username:
        form = FeedbackForm()
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username=session["username"],
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{username}")
    flash("Please login to add feedback!")
    return redirect("/")


@app.route("/feedback/<int:feedback_id>/update", methods=["GET"])
def show_update_feedback(feedback_id):
    """Shows update feedback form"""
    current_feedback = Feedback.query.get_or_404(feedback_id)
    if "username" in session and session["username"] == current_feedback.username:
        form = FeedbackForm(obj=current_feedback)
        return render_template(
            "update_feedback_form.html", current_feedback=current_feedback, form=form
        )
    flash("Please login to edit feedback!")
    return redirect("/")


@app.route("/feedback/<int:feedback_id>/update", methods=["POST"])
def update_feedback(feedback_id):
    """updates feedback"""
    current_feedback = Feedback.query.get_or_404(feedback_id)
    if "username" in session and session["username"] == current_feedback.username:
        form = FeedbackForm()
        if form.validate_on_submit():
            current_feedback.title = form.title.data
            current_feedback.content = form.content.data
            db.session.add(current_feedback)
            db.session.commit()
            return redirect(f"/users/{current_feedback.username}")
        return redirect(f"/feedback/{feedback_id}/update")
    flash("Please login to edit feedback!")
    return redirect("/")


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Deletes feedback"""
    current_feedback = Feedback.query.get_or_404(feedback_id)
    if "username" in session and session["username"] == current_feedback.username:
        Feedback.query.filter_by(id=feedback_id).delete()
        db.session.commit()
        return redirect(f"/users/{current_feedback.username}")
    flash("Please login to delete feedback!")
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    """Shows 404 page"""
    return (render_template("404.html"), 404)

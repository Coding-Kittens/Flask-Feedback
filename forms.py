from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20, message="Username can not have more than 20 characters"),
        ],
    )
    password = PasswordField("Password", validators=[InputRequired()])


class SignUpForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20, message="Username can not have more than 20 characters"),
        ],
    )
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(),
            Length(max=30, message="Fist Name can not have more than 30 characters"),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(),
            Length(max=30, message="Last Name can not have more than 30 characters"),
        ],
    )


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

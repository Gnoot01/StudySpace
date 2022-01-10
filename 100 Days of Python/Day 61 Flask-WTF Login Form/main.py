"""
requirements.txt specifies all dependencies and their versions, so can simply share and run in terminal
'pip install Flask-WTF' to download
'pip install email_validator' for email validator
'pip install Flask-Bootstrap' for flask-bootstrap
"""

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_bootstrap import Bootstrap


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[validators.DataRequired(), validators.Email(message="Invalid email address")])
    password = PasswordField(label='Password', validators=[validators.DataRequired(), validators.Length(min=8, message="Input must be at least %(min)d characters long")])
                # Obscures into |***|          |accepts list of validator objects|required field|validating email & password
    submit = SubmitField(label="Log In")


app = Flask(__name__)
app.secret_key = "secret"
Bootstrap(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit(): # = from flask import request+checking if request.method == "POST", as validate_on_submit() only returns True if successfully validated after form submission, only allowed by POST
        if login_form.email.data == "iusdhhihgushfuogf@gmail.com" and login_form.password.data == "12345678": return render_template("success.html") # = request.form["email/password"]
        return render_template("denied.html")
    return render_template('login.html', form=login_form)


if __name__ == '__main__': app.run(debug=True)
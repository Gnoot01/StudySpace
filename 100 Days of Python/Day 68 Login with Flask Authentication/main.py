from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# restores a user from user_id stored in the session
@login_manager.user_loader
def load_user(id:int):
    return User.query.get(id)


# UserMixin: provides multiple inheritance, with required methods is_authenticated, is_active, is_anonymous and get_id()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user:
            if check_password_hash(user.password, request.form["password"]):
                login_user(user, remember=False, duration=None)
                flash('Logged in successfully.')
                return redirect(url_for('secrets'))
            flash('Password incorrect, please try again')
            return redirect(url_for('login'))
        # User doesn't exist in db
        flash("User doesn't exist, please register first")
        return redirect(url_for('register'))
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            new_user = User(name=request.form["name"],
                            email=request.form["email"],
                            password=generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8)
                        )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False, duration=None)
            flash('Registered successfully.')
            return redirect(url_for('secrets'))
        # Creating a new_user with same unique email
        except IntegrityError:
            flash("You already have an account with that email. Log in instead!")
            return redirect(url_for('login'))
    return render_template("register.html")


@app.route('/secrets')
# @fresh_login_required to ensure user’s login is fresh (session not restored from a ‘remember me’ cookie). For sensitive operations like changing login details
# login_required: a decorator, current_user: retrieves current_user data
@login_required
def secrets():
    # no longer need a <name> in route or secrets(name) parameter cos @login_required ensures logged in, from which current_user.name is retrieved
    return render_template("secrets.html", name=current_user.name, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(directory='static', path='files/cheat_sheet.pdf')


if __name__ == "__main__": app.run(debug=True)

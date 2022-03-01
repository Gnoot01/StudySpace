"""
'pip install flask_gravatar'
Gravatar images to auto-gen an avatar image for blog commenters.
Can add https://www.perfecttense.com/api to CKEditor to enable grammar, spelling, tense, sentence structure check
"""
from flask import Flask, render_template, redirect, url_for, flash, abort
from functools import wraps
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship 
from sqlalchemy.exc import IntegrityError
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, CommentForm, RegisterForm, LoginForm
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
ckeditor = CKEditor(app)
gravatar = Gravatar(app, size=100, rating='x', default='wavatar', force_default=False, force_lower=False, use_ssl=False, base_url=None)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id:int):
    return User.query.get(id)


# Creating @admin_only decorator
def admin_only(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Abort if user is not admin. Else continue
        if current_user.id != 1: return abort(403)
        return f(*args, **kwargs)
    return decorator


# SQLite, MySQL, Postgresql can create relational dbs where 1 user can have many blogposts, but those blogposts can only have 1 user to reveal all his posts (1-many<->many-1)
# Unlike a simple class where latter can't be done. Read: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
class User(UserMixin, db.Model):
    # Creating diff tables in same sql .db file
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    #                      class      refers back to class BlogPost attribute -> relationship=now a BlogPost object
    posts = relationship("BlogPost", back_populates="post_author")
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    #                                             table PK attribute
    post_author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #                      class     refers back to class User attribute -> relationship=now a User object, HENCE can tap into {{post.post_author.name}}
    post_author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    comment_author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_author = relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    parent_post = relationship("BlogPost", back_populates="comments")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    # Instead of passing in logged_in=..., user_id=... to check in .html, simply pass in current_user=current_user & check current_user.is_authenticated/.id in .html itself
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        try:
            new_user = User(email=register_form.email.data,
                            password=generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8),
                            name=register_form.name.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False, duration=None)
            return redirect(url_for('get_all_posts'))
        except IntegrityError:
            flash("An account with that email already exists, log in instead!")
            return redirect(url_for('login'))
    return render_template("register.html", form=register_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    user = User.query.filter_by(email=login_form.email.data).first()
    if login_form.validate_on_submit():
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user, remember=False, duration=None)
                return redirect(url_for('get_all_posts'))
            flash("Password incorrect, please try again!")
            return redirect(url_for('login'))
        flash("Sorry, that email does not exist, please register first!")
        return redirect(url_for('register'))
    return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            db.session.add(Comment(text=comment_form.body.data,
                                   comment_author_id=current_user.id,
                                   post_id=post_id))
            db.session.commit()
            flash("Commented Successfully!")
            return redirect(url_for('show_post', post_id=post_id))
        flash("You need to login or register to comment")
        return redirect(url_for('login'))
    return render_template("post.html", form=comment_form, post=requested_post, current_user=current_user)


@app.route("/new-post", methods=["GET", "POST"])
# To make passing in current_user=current_user & checking if current_user.is_authenticated in make-post.html redundant since @login_required ensures already.
@login_required
# Non-admins can't see the buttons but can still manually access the protected routes. So set @admin_only
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        db.session.add(BlogPost(title=form.title.data,
                                subtitle=form.subtitle.data,
                                body=form.body.data,
                                img_url=form.img_url.data,
                                post_author_id=current_user.id,
                                date=datetime.date.today().strftime("%B %d, %Y")
                            ))
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, is_edit=False)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/delete/<int:post_id>/<int:comment_id>", methods=["GET", "POST"])
@login_required
@admin_only
def delete_comment(post_id, comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))


@app.route("/search/<int:post_author_id>")
def search_author_posts(post_author_id):
    return render_template('index.html', all_posts=BlogPost.query.filter_by(post_author_id=post_author_id))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__": app.run(debug=True)

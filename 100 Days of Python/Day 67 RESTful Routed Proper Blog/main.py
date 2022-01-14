"""
'pip install flask_ckeditor' for full fledged text editor on website
"""
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from flask_ckeditor import CKEditor, CKEditorField
import datetime

 
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[validators.DataRequired()])
    subtitle = StringField("Subtitle", validators=[validators.DataRequired()])
    author = StringField("Your Name", validators=[validators.DataRequired()])
    img_url = StringField("Blog Image URL", validators=[validators.DataRequired(), validators.URL()])
    # CKEditorField data saved as HTML, containing structure & styling of blog, but default renders as text (with all HTML tags <p>, etc)
    # HENCE need to add {{ post.body|safe }} filter in post.html to render as HTML instead
    body = CKEditorField("Blog Content", validators=[validators.DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:id>")
def show_post(id):
    return render_template("post.html", post=BlogPost.query.get(id))


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    create_post_form = CreatePostForm()
    if create_post_form.validate_on_submit():
        db.session.add(BlogPost(title=create_post_form.title.data,
                                date=datetime.datetime.now().strftime("%B %d, %Y"),
                                body=create_post_form.body.data,
                                author=create_post_form.author.data,
                                img_url=create_post_form.img_url.data,
                                subtitle=create_post_form.subtitle.data,
                                ))
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=create_post_form, to_create_post=True)


# While this normally would be "PUT/PATCH" request, HTML/WTForms only accept "GET"&"POST" requests
@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post_to_edit = BlogPost.query.get(id)
    # to auto-populate form with previous content so no need to re-write again
    edit_post_form = CreatePostForm(
        title=post_to_edit.title,
        body=post_to_edit.body,
        author=post_to_edit.author,
        img_url=post_to_edit.img_url,
        subtitle=post_to_edit.subtitle,
        )
    if edit_post_form.validate_on_submit():
        post_to_edit.title=edit_post_form.title.data
        post_to_edit.body = edit_post_form.body.data
        post_to_edit.img_url = edit_post_form.img_url.data
        post_to_edit.author = edit_post_form.author.data
        post_to_edit.subtitle = edit_post_form.subtitle.data
        db.session.commit()
        return redirect(url_for('show_post', id=id))
    return render_template('make-post.html', form=edit_post_form, to_create_post=False)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_post(id):
    db.session.delete(BlogPost.query.get(id))
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/search/<author>", methods=["GET", "POST"])
def search_author_posts(author):
    return render_template('index.html', all_posts=BlogPost.query.filter_by(author=author))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__": app.run(debug=True)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[validators.DataRequired()])
    subtitle = StringField("Subtitle", validators=[validators.DataRequired()])
    img_url = StringField("Blog Image URL", validators=[validators.DataRequired(), validators.URL()])
    body = CKEditorField("Blog Content", validators=[validators.DataRequired()])
    submit = SubmitField("Submit Post")


class CommentForm(FlaskForm):
    body = CKEditorField("Comment", validators=[validators.DataRequired()])
    submit = SubmitField("Submit Comment")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email(message="Invalid email address")])
    password = PasswordField(label='Password', validators=[validators.DataRequired(), validators.Length(min=8, message="Input must be at least %(min)d characters long")])
    name = StringField("Name", validators=[validators.DataRequired()])
    submit = SubmitField(label="Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email(message="Invalid email address")])
    password = PasswordField(label='Password', validators=[validators.DataRequired()])
    submit = SubmitField(label="Let Me In!")
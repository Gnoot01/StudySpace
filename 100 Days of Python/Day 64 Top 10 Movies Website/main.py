from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, validators
import requests


# Get from https://www.themoviedb.org/>Settings>API
API_KEY = "..."
MDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie/"
MDB_INFO_URL = "https://api.themoviedb.org/3/movie"
MDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
# Execute once
# db.create_all()


class RateMovieForm(FlaskForm):
    rating = FloatField(label='Your Rating out of 10 eg: 7.5', validators=[validators.DataRequired(), validators.NumberRange(min=0, max=10, message="Input must be between %(min)d - %(max)d inclusive")])
    # for optional field, can remove validators / validate Optional (halts validation chain, so put it at last)
    review = StringField(label='Your Review', validators=[validators.Optional()])
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[validators.DataRequired()])
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    # sorted by descending order
    all_movies = db.session.query(Movie).order_by(Movie.rating.desc()).all()
    # cos gives a list - index starts from 0, so need to Update again
    for movie in all_movies: movie.ranking = all_movies.index(movie) + 1
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    id = request.args.get("id", type=int)
    movie_to_edit = Movie.query.get(id)
    rate_movie_form = RateMovieForm()
    if rate_movie_form.validate_on_submit():
        movie_to_edit.rating = rate_movie_form.rating.data
        # If review already exists (tagline), I want review to be optional and still show tagline, unless I want to change review
        if rate_movie_form.review.data != "" and rate_movie_form.review.data != movie_to_edit.review: movie_to_edit.review = rate_movie_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=rate_movie_form, movie_to_edit=movie_to_edit)


@app.route("/delete")
def delete():
    id = request.args.get("id", type=int)
    movie_to_del = Movie.query.get(id)
    db.session.delete(movie_to_del)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        PARAMS = {
            "api_key": API_KEY,
            "include_adult": "true",
            "query": add_movie_form.title.data,
        }
        add_movie_data = requests.get(MDB_SEARCH_URL, params=PARAMS).json()["results"]
        return render_template("select.html", add_movie_data=add_movie_data)
    return render_template("add.html", form=add_movie_form)


@app.route("/search")
def search():
    PARAMS = {
        "api_key": API_KEY,
    }
    # api endpoint is .../83218?api_key=... NOT .../?movie_id=83218&api_key=...
    movie_to_add = requests.get(f"{MDB_INFO_URL}/{request.args.get('id', type=int)}", params=PARAMS).json()
    # Rating, Ranking missing
    new_movie = Movie(
        title=movie_to_add["title"],
        year=int(movie_to_add["release_date"].split("-")[0]),
        description=movie_to_add["overview"],
        review=f"Fav quote - {movie_to_add['tagline']}",
        img_url=f"{MDB_IMAGE_URL}{movie_to_add['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))

 
if __name__ == '__main__': app.run(debug=True)

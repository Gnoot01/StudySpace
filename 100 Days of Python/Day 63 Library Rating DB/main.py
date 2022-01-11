from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template("index.html", all_books=db.session.query(Book).all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        db.session.add(Book(title=request.form["title"], author=request.form["author"], rating=float(request.form["rating"])))
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    id = request.args.get('id', type=int)  # to get url to be /edit?id=_, GET's variation of POST request.form[""]
    book_to_edit = Book.query.get(id)
    if request.method == "POST":
        book_to_edit.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book_to_edit=book_to_edit)

    # If edit.html uses hidden field for id instead
    # if request.method == "POST":
    #     Book.query.get(request.form["id"]).rating = request.form["rating"]
    #     db.session.commit()
    #     return redirect(url_for('home'))
    # id = request.args.get('id', type=int)
    # book_to_edit = Book.query.get(id)
    # return render_template("edit.html", book_to_edit=book_to_edit)


@app.route("/delete")
def delete():
    id = request.args.get('id', type=int)
    db.session.delete(Book.query.get(id))
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__": app.run(debug=True)


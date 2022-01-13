"""
Instead of testing API with parameters by typing them all out in URL,
use Postman:https://www.postman.com/downloads/ to add key-value pairs for request parameters and auto format URL
To make POST request: POST>Body>x-www-form-urlencoded, basically <body><form action=... method=...><input name=k value=v>... for k-v pair
Save all requests, name & describe them in Postman>Publish to auto generate API documentation: https://documenter.getpostman.com/view/19140750/UVXhqcPC
"""
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # Method 2: to_dict()
    def to_dict(self):
        # Simpler but less control (no amenities)
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}
        data = {"amenities": {}}
        for column in self.__table__.columns:
            if column.name in ["name", "map_url", "img_url", "location"]: data[column.name] = getattr(self, column.name)
            else: data["amenities"][column.name] = getattr(self, column.name)
        return data


def str_to_bool(v):
    if v in ['True', 'true', 'T', 't', 'Yes', 'yes', 'Y', 'y', '1']: return True
    return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    # random_cafe = random.choice(Cafe.query.all())
    # VS for speed, scalability:
    random_cafe = Cafe.query.offset(random.randint(0, Cafe.query.count()-1)).first()

    # Serialization: random_cafe SQLAlchemy Object -> JSON
    # Method 1: typing it all out +: more control -:tedious & repetitive, esp for more routes
    # return jsonify(cafe={
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "amenities": {
    #         "has_sockets": random_cafe.has_sockets,
    #         "has_toilet": random_cafe.has_toilet,
    #         "has_wifi": random_cafe.has_wifi,
    #         "can_take_calls": random_cafe.can_take_calls,
    #         "seats": random_cafe.seats,
    #         "coffee_price": random_cafe.coffee_price,},
    # })
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all():
    return jsonify(cafes=[cafe.to_dict() for cafe in Cafe.query.all()])


@app.route("/search")
def search():
    query_location = request.args.get("loc")
    found_cafe = Cafe.query.filter_by(location=query_location).first()
    if found_cafe: return jsonify(cafe=found_cafe.to_dict())
    return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/add", methods=["POST"])
def add():
    db.session.add(Cafe(name=request.form["name"],
                        map_url=request.form["map_url"],
                        img_url=request.form["img_url"],
                        location=request.form["location"],
                        # Need str_to_bool as request.form[] returns string of which is t/y/1, etc. If empty, returns False
                        has_sockets=str_to_bool(request.form["has_sockets"]),
                        has_toilet=str_to_bool(request.form["has_toilet"]),
                        has_wifi=str_to_bool(request.form["has_wifi"]),
                        can_take_calls=str_to_bool(request.form["can_take_calls"]),
                        seats=request.form["seats"],
                        coffee_price=request.form["coffee_price"],))
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe_to_update = Cafe.query.get(cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    # Need to pass an HTTP code with response, else even if error, will return success code 200
    return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    api_key = request.args.get("api_key")
    if api_key == "TopSecretAPIKey":
        cafe_to_delete = Cafe.query.get(cafe_id)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe."}), 200
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404
    return jsonify(error={"Not Authorised": "Sorry, you're not authorised. Make sure you have the correct api_key"}), 403


if __name__ == '__main__': app.run(debug=True)

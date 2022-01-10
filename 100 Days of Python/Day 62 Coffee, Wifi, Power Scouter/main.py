"""
requirements.txt specifies all dependencies and their versions, so can simply share and run in terminal
'pip install Flask-WTF' to download
'pip install email_validator' for Email validator
'pip install Flask-Bootstrap' for flask-bootstrap
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, validators
import csv

app = Flask(__name__)
app.secret_key = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# OR app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[validators.DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[validators.DataRequired(), validators.URL(message="Invalid URL")])
    opening_time = StringField('Opening Time e.g.8AM', validators=[validators.DataRequired()])
    closing_time = StringField('Closing Time e.g.5:30PM', validators=[validators.DataRequired()])
    # I think there's no need for DataRequired() for below options, cos the default is already chosen, there's no way to have empty field anyways
    coffee = SelectField('Coffee Rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi = SelectField('Wifi Strength Rating', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField('Power Socket Availability', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},{form.location.data},{form.opening_time.data},{form.closing_time.data},{form.coffee.data},{form.wifi.data},{form.power.data}")
        return render_template('add.html', form=form, successful=True)
    return render_template('add.html', form=form, successful=False)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data: list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__': app.run(debug=True)

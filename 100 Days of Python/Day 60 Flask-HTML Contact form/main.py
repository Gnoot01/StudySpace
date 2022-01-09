from flask import Flask, render_template, request
import requests
import smtplib


app = Flask(__name__)
posts = requests.get("https://api.npoint.io/010a7708385076377389").json()
EMAIL = "pythontestosterone@gmail.com"
PASSWORD = "..."

@app.route("/")
@app.route("/index.html")
# for some reason, website loads .../index.html instead of .../index
def home():
    return render_template("index.html", posts=posts)

@app.route("/post/<int:id>")
def get_post(id):
    req_post = None
    for post in posts:
        if post["id"] == id: req_post = post
    return render_template("post.html", post=req_post)


@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject:New Message\n\nName: {request.form['name']}\nEmail: {request.form['email']}\nPhone: {request.form['phone']}\nMessage: {request.form['msg']}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


if __name__ == "__main__": app.run(debug=True)

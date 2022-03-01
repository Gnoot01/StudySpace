from flask import Flask, render_template
import requests
from post import Post

posts = requests.get("https://api.npoint.io/46c980af38f59842b5b7").json()
post_objects = [Post(post["id"], post["title"], post["subtitle"], post["body"]) for post in posts]
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", post_objects=post_objects)

# Very impt snippet of code to click on post & get result
@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    req_post = None
    for post in post_objects:
        if post.id == blog_id: req_post = post
    return render_template("post.html", req_post=req_post)


if __name__ == "__main__": app.run(debug=True)
#################################################################################################################################################################################
# An alternative to creating a custom class 'Post' and instead just using in-built Flask . method
from flask import Flask, render_template
import requests

posts = requests.get("https://api.npoint.io/46c980af38f59842b5b7").json()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=posts)

# Very impt snippet of code to click on post & get result
@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    req_post = None
    for post in posts:
        if post["id"] == blog_id: req_post = post
    return render_template("post.html", post=req_post)


if __name__ == "__main__": app.run(debug=True)


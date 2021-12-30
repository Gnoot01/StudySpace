from flask import Flask
import random
app = Flask(__name__)
CHOSEN_NUM = random.randint(0, 9)

@app.route("/")
def hello_world():
    return "<h1>Guess a number between 0 and 9 using url</h1>" \
           "<img src=https://media0.giphy.com/media/qVx82Zydz2dVRrok6t/giphy.gif?cid=790b7611e876c171a190e6e6ef54350f15b3b45d023a733a&rid=giphy.gif&ct=g alt=Mystery Num!>"

@app.route("/<int:num>")
def check_num(num):
    if num < CHOSEN_NUM: return "<h1 style='color: red'>Too low, try again!</h1>" \
                                "<img src=https://media4.giphy.com/media/r7yLWxRd640zC/giphy.gif?cid=790b76110794c5ac932dd2c37fe440b1da573e71ac75de25&rid=giphy.gif&ct=g alt=Puppy fail>"
    elif num > CHOSEN_NUM: return "<h1 style='color: purple'>Too high, try again!</h1>" \
                                "<img src=https://media4.giphy.com/media/Vp9rYcsH1cIVO/giphy.gif?cid=ecf05e47ts4f5pwk5n71sbk1grnk9j4vtt2p58c85lj3wfij&rid=giphy.gif&ct=g alt=Puppy fail>"
    return "<h1 style='color: green'>You found me!</h1>" \
           "<img src=https://media4.giphy.com/media/l0unkiodQqmA3lPO5e/giphy.gif?cid=ecf05e47jgktgej5f5kctmjbgrj6qbufc9470szvmi4knw3k&rid=giphy.gif&ct=g alt=Puppy success>"


if __name__ == "__main__": app.run(debug=True)

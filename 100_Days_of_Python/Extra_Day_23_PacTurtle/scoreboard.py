from turtle import Turtle
from pacturtle import PacTurtle
import time

LIVES_LOCATION = [(-280, -105), (-260, -105), (-240, -105)]

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.live3 = PacTurtle()
        self.live2 = PacTurtle()
        self.live1 = PacTurtle()
        self.lives = [self.live1, self.live2, self.live3]
        self.setup()

    def setup(self):
        self.hideturtle()
        self.penup()
        # How to make blinking logo effect?
        self.display_logo()
        self.display_score()
        # How to initially display 3 lives, but once game starts, display 2?
        self.display_lives()
        self.display_cherry()
        self.color("red")
        self.display_ready()

    def display_logo(self):
        logo = Turtle()
        logo.color("white")
        logo.hideturtle()
        logo.penup()
        logo.goto(-280, 95)
        logo.write("1UP", align="left", font=("Courier", 8))

    def display_score(self):
        self.color("white")
        self.goto(-280, 85)
        self.write(f"{self.score}", align="left", font=("Courier", 8))

    def increase_score(self, increase):
        self.score += increase
        self.clear()
        self.display_score()

    def display_lives(self):
        for live in self.lives:
            live.showturtle()
            live.create_pacturtle()
            live.spawn_at(LIVES_LOCATION[self.lives.index(live)])

    def decrease_lives(self):
        for live in self.lives:
            live.hideturtle()
        if len(self.lives) > 0:
            del self.lives[-1]
        self.display_lives()

    def display_cherry(self):
        cherry = Turtle()
        cherry.hideturtle()
        cherry.penup()
        cherry.goto(270, -105)
        cherry.dot(9, "red")

    def display_ready(self):
        self.goto(70, -35)
        self.write("READY!", align="center", font=("Courier", 10))
        time.sleep(1)

    def game_over(self):
        self.goto(70, -35)
        self.write("GAME OVER.", align="center", font=("Ariel", 20))

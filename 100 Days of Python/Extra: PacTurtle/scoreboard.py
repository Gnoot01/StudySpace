from turtle import Turtle, Screen
from food import Food
from pacturtle import PacTurtle
import time

LIVES_LOCATION = [(-280, -105), (-260, -105), (-240, -105)]

class ScoreBoard():
    def __init__(self):
        self.score = 0
        self.score_print = Turtle()
        self.live3 = PacTurtle()
        self.live2 = PacTurtle()
        self.live1 = PacTurtle()
        self.lives = [self.live1, self.live2, self.live3]
        self.setup()

    def setup(self):
        self.display_logo()
        self.display_score()
        self.update_lives()
        self.display_ready()
        # food = Food()
        # food.setup_cherry()

    def display_ready(self):
        ready = Turtle()
        ready.hideturtle()
        ready.color("red")
        ready.penup()
        ready.goto(70, -35)
        ready.write("READY!", align="center", font=("Ariel", 10))
        time.sleep(1)
        ready.clear()

    # How to make blinking effect?
    def display_logo(self):
        logo = Turtle()
        logo.hideturtle()
        logo.color("white")
        logo.penup()
        logo.goto(-280, 95)
        logo.write("1UP", align="left", font=("Ariel", 8))

    def display_score(self):
        self.score_print.clear()
        self.score_print.hideturtle()
        self.score_print.color("white")
        self.score_print.penup()
        self.score_print.goto(-280, 85)
        self.score_print.write(f"{self.score}", align="left", font=("Ariel", 8))

    def increase_score(self, increase):
        self.score += increase
        self.display_score()

    # How to initially display 3, but once game starts, display 2?
    def update_lives(self):
        for live in self.lives:
            live.showturtle()
            live.create_pacturtle()
            live.spawn_at(LIVES_LOCATION[self.lives.index(live)])



    def decrease_lives(self):
        for live in self.lives:
            live.hideturtle()
        if len(self.lives) > 0:
            del self.lives[-1]
        self.update_lives()

    def game_over(self):
        self.goto(70, -35)
        self.write("GAME OVER.", align="center", font=("Ariel", 15))

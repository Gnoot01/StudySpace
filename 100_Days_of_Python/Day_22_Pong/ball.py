from turtle import Turtle
import random

# Idea: Uncomment all pen related to allow tracing of ball path, might make interesting art esp if played by someone renowned
# See ponGArt.png

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        #self.pendown()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.04


    def move(self):
        self.goto(self.xcor()+self.x_move, self.ycor()+self.y_move)

    def increase_speed(self):
        self.x_move += 1

    def x_bounce(self):
        self.x_move *= -1
        self.move_speed *= 0.9

    def y_bounce(self):
        self.y_move *= -1

    def reset(self):
        #self.penup()
        #self.pencolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.goto((0, 0))
        self.move_speed = 0.04
        self.x_bounce()
        #self.pendown()





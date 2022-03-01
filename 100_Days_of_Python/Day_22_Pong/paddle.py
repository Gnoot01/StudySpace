from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, coords):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed("fastest")
        self.shapesize(stretch_len=5)
        self.setheading(90)
        self.goto(coords)

    def move_up(self):
        self.setheading(90)
        self.forward(30)

    def move_down(self):
        self.setheading(270)
        self.forward(30)

    def maintain(self):
        if self.ycor() > 250: self.goto(self.xcor(), 250)
        if self.ycor() < -250: self.goto(self.xcor(), -250)

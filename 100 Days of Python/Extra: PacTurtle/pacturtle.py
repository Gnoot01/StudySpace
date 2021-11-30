from turtle import Turtle
MOVE_DISTANCE = 5

# Pacman animation: https://www.youtube.com/watch?v=cJGwQwlH-Pw

class PacTurtle(Turtle):
    def __init__(self):
        super().__init__()
        self.create_pacturtle()
        self.spawn_at((70, -75))

    def create_pacturtle(self):
        self.shape("turtle")
        self.shapesize(stretch_len=0.65, stretch_wid=0.65)
        self.color("yellow")
        self.penup()
        self.turn_west()

    def spawn_at(self, location):
        self.goto(location)

    def move(self):
        self.forward(MOVE_DISTANCE)

    def turn_north(self):
        self.setheading(90)

    def turn_south(self):
        self.setheading(270)

    def turn_west(self):
        self.setheading(180)

    def turn_east(self):
        self.setheading(0)


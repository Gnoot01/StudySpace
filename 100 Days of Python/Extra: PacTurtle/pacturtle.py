import time
from turtle import Turtle
MOVE_DISTANCE = 5

# Inherit only if creating 1 object/instancing multiple objects with SAME states -> can modify all with self.
# If creating multiple objects/instancing multiple objects with DIFF states (food,scoreboard), cannot inherit, cannot modify all with self.

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

        # Animate pacman: https://www.youtube.com/watch?v=cJGwQwlH-Pw
        # not entirely sure how to use this though...

        # while True:
        #     for n in [0, 30]:
        #         self.penup()
        #         self.color("yellow")
        #         self.goto(70, -75)
        #         self.speed(11)
        #         self.hideturtle()
        #         self.left(150)
        #         self.begin_fill()
        #         self.circle(50, 270+n)
        #         self.left(90)
        #         self.forward(50)
        #         self.right(90)
        #         self.forward(50)
        #         self.end_fill()
        #         time.sleep(0.1)
        #         if n == 30: self.clear()
        #         return False

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

    def tp_l_to_r(self):
        self.goto(280, -5)

    def tp_r_to_l(self):
        self.goto(-280, -5)

    # Pacman speed increase aft eating powerup to chase ghosts easier

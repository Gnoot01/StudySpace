from turtle import Turtle

STARTING_POS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
NORTH = 90
SOUTH = 270
EAST = 0
WEST = 180

class Snake:

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POS:
            self.add_segment(position)

    def add_segment(self, position):
        segment = Turtle(shape="square")
        segment.color("white")
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def grow(self):
        self.add_segment(self.segments[-1].pos())

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            # |3|2|1|, |3| goes to |2| position, |2| goes to |1| position, so that they're following the head |1| instead of
            # being detached and moving by themselves
            new_x = self.segments[i - 1].xcor()
            new_y = self.segments[i - 1].ycor()
            self.segments[i].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def turn_north(self):
        if self.head.heading() != SOUTH: self.head.setheading(90)

    def turn_south(self):
        if self.head.heading() != NORTH: self.head.setheading(270)

    def turn_west(self):
        if self.head.heading() != EAST: self.head.setheading(180)

    def turn_east(self):
        if self.head.heading() != WEST: self.head.setheading(0)

    def teleport_right_to_left(self):
        self.head.goto(-500, self.head.ycor())

    def teleport_left_to_right(self):
        self.head.goto(500, self.head.ycor())

    def teleport_up_to_down(self):
        self.head.goto(self.head.xcor(), -400)

    def teleport_down_to_up(self):
        self.head.goto(self.head.xcor(), 400)




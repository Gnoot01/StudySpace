from turtle import Turtle

class Walls():

    def __init__(self):
        self.pen1 = Turtle()
        self.pen2 = Turtle()
        self.prepare_pens()
        self.draw()

    def prepare_pens(self):
        for pen in [self.pen1, self.pen2]:
            pen.color("blue")
            pen.speed("fastest")
            pen.hideturtle()
            pen.penup()

    def draw(self):
        self.draw_outerwall()
        self.draw_obstacles()
        self.draw_google()

    def draw_outerwall(self):
        # Top half
        self.pen1.goto((-280, 5))
        self.pen1.pendown()
        self.pen2.goto((-280, 10))
        self.pen2.pendown()
        self.pen1.goto((-240, 5))
        self.pen2.goto((-245, 10))
        self.pen1.goto((-240, 25))
        self.pen2.goto((-245, 20))
        self.pen1.goto((-280, 25))
        self.pen2.goto((-285, 20))
        self.pen1.goto((-280, 75))
        self.pen2.goto((-285, 80))
        self.pen1.goto((280, 75))
        self.pen2.goto((285, 80))
        self.pen1.goto((280, 25))
        self.pen2.goto((285, 20))
        self.pen1.goto((240, 25))
        self.pen2.goto((245, 20))
        self.pen1.goto((240, 5))
        self.pen2.goto((245, 10))
        self.pen1.goto((280, 5))
        self.pen2.goto((280, 10))
        self.pen1.penup()
        self.pen2.penup()
        # Bottom half
        self.pen1.goto((280, -15))
        self.pen1.pendown()
        self.pen2.goto((280, -20))
        self.pen2.pendown()
        self.pen1.goto((240, -15))
        self.pen2.goto((245, -20))
        self.pen1.goto((240, -35))
        self.pen2.goto((245, -30))
        self.pen1.goto((280, -35))
        self.pen2.goto((285, -30))
        self.pen1.goto((280, -85))
        self.pen2.goto((285, -90))
        # Obstacle 1 R->L
        self.pen1.goto((100, -85))
        self.pen1.goto((100, -65))
        self.pen1.goto((90, -65))
        self.pen1.goto((90, -85))
        # Obstacle 2
        self.pen1.goto((50, -85))
        self.pen1.goto((50, -65))
        self.pen1.goto((40, -65))
        self.pen1.goto((40, -85))
        # Obstacle 3
        self.pen1.goto((-90, -85))
        self.pen1.goto((-90, -55))
        self.pen1.goto((-100, -55))
        self.pen1.goto((-100, -85))
        #
        self.pen1.goto((-280, -85))
        self.pen2.goto((-285, -90))
        self.pen1.goto((-280, -35))
        self.pen2.goto((-285, -30))
        self.pen1.goto((-240, -35))
        self.pen2.goto((-245, -30))
        self.pen1.goto((-240, -15))
        self.pen2.goto((-245, -20))
        self.pen1.goto((-280, -15))
        self.pen2.goto((-280, -20))
        self.pen1.penup()
        self.pen2.penup()

    def draw_obstacles(self):
        # Top half obstacles
        self.pen1.goto((-260, 55))
        self.pen1.pendown()
        self.pen1.goto((-240, 55))
        self.pen1.goto((-240, 45))
        self.pen1.goto((-260, 45))
        self.pen1.goto((-260, 55))
        self.pen1.penup()
        self.pen1.goto((-120, 55))
        self.pen1.pendown()
        self.pen1.goto((20, 55))
        self.pen1.goto((20, 45))
        self.pen1.goto((-120, 45))
        self.pen1.goto((-120, 55))
        self.pen1.penup()
        self.pen1.goto((50, 55))
        self.pen1.pendown()
        self.pen1.goto((100, 55))
        self.pen1.goto((100, 45))
        self.pen1.goto((50, 45))
        self.pen1.goto((50, 55))
        self.pen1.penup()
        self.pen1.goto((160, 55))
        self.pen1.pendown()
        self.pen1.goto((200, 55))
        self.pen1.goto((200, 45))
        self.pen1.goto((160, 45))
        self.pen1.goto((160, 55))
        self.pen1.penup()
        self.pen1.goto((220, 55))
        self.pen1.pendown()
        self.pen1.goto((260, 55))
        self.pen1.goto((260, 45))
        self.pen1.goto((220, 45))
        self.pen1.goto((220, 55))
        self.pen1.penup()

        # Bottom half obstacles
        self.pen1.goto((-260, -55))
        self.pen1.pendown()
        self.pen1.goto((-230, -55))
        self.pen1.goto((-230, -65))
        self.pen1.goto((-260, -65))
        self.pen1.goto((-260, -55))
        self.pen1.penup()
        self.pen1.goto((-210, -55))
        self.pen1.pendown()
        self.pen1.goto((-120, -55))
        self.pen1.goto((-120, -65))
        self.pen1.goto((-210, -65))
        self.pen1.goto((-210, -55))
        self.pen1.penup()
        self.pen1.goto((-70, -55))
        self.pen1.pendown()
        self.pen1.goto((20, -55))
        self.pen1.goto((20, -65))
        self.pen1.goto((-70, -65))
        self.pen1.goto((-70, -55))
        self.pen1.penup()
        # T obstacle
        self.pen1.goto((40, -35))
        self.pen1.pendown()
        self.pen1.goto((100, -35))
        self.pen1.goto((100, -45))
        self.pen1.goto((75, -45))
        self.pen1.goto((75, -65))
        self.pen1.goto((65, -65))
        self.pen1.goto((65, -45))
        self.pen1.goto((40, -45))
        self.pen1.goto((40, -35))
        self.pen1.penup()
        #
        self.pen1.goto((120, -55))
        self.pen1.pendown()
        self.pen1.goto((200, -55))
        self.pen1.goto((200, -65))
        self.pen1.goto((120, -65))
        self.pen1.goto((120, -55))
        self.pen1.penup()
        self.pen1.goto((220, -55))
        self.pen1.pendown()
        self.pen1.goto((260, -55))
        self.pen1.goto((260, -65))
        self.pen1.goto((220, -65))
        self.pen1.goto((220, -55))
        self.pen1.penup()

    def draw_google(self):
        # G
        self.pen1.goto((-220, 55))
        self.pen1.pendown()
        self.pen1.goto((-140, 55))
        self.pen1.goto((-140, 35))
        self.pen1.goto((-200, 35))
        self.pen1.goto((-200, -15))
        self.pen1.goto((-160, -15))
        self.pen1.goto((-160, 5))
        self.pen1.goto((-180, 5))
        self.pen1.goto((-180, 15))
        self.pen1.goto((-140, 15))
        self.pen1.goto((-140, -35))
        self.pen1.goto((-220, -35))
        self.pen1.goto((-220, 55))
        self.pen1.penup()
        # o
        self.pen1.color("red")
        self.pen2.color("red")
        self.pen1.goto((-120, -35))
        self.pen1.pendown()
        self.pen1.goto((-60, -35))
        self.pen1.goto((-60, 25))
        self.pen1.goto((-120, 25))
        self.pen1.goto((-120, -35))
        self.pen2.goto((-100, -15))
        self.pen2.pendown()
        self.pen2.goto((-80, -15))
        self.pen2.goto((-80, 5))
        self.pen2.goto((-100, 5))
        self.pen2.goto((-100, -15))
        self.pen1.penup()
        self.pen2.penup()
        # o
        self.pen1.color("yellow")
        self.pen2.color("yellow")
        self.pen1.goto((-40, -35))
        self.pen1.pendown()
        self.pen1.goto((20, -35))
        self.pen1.goto((20, 25))
        self.pen1.goto((-40, 25))
        self.pen1.goto((-40, -35))
        self.pen2.goto((-20, -15))
        self.pen2.pendown()
        self.pen2.goto((0, -15))
        self.pen2.goto((0, 5))
        self.pen2.goto((-20, 5))
        self.pen2.goto((-20, -15))
        self.pen1.penup()
        self.pen2.penup()
        # Ghost cage
        self.pen1.color("blue")
        self.pen2.color("blue")
        self.pen1.goto((40, -15))
        self.pen1.pendown()
        self.pen2.goto((45, -10))
        self.pen2.pendown()
        self.pen1.goto((100, -15))
        self.pen2.goto((95, -10))
        self.pen1.goto((100, 25))
        self.pen1.goto((80, 25))
        self.pen1.penup()
        self.pen1.color("orange")
        self.pen1.pendown()
        self.pen1.goto((80, 25))
        self.pen1.goto((60, 25))
        self.pen1.goto((60, 20))
        self.pen1.goto((80, 20))
        self.pen1.goto((80, 25))
        self.pen1.penup()
        self.pen1.color("blue")
        self.pen1.goto((60, 25))
        self.pen1.pendown()
        self.pen1.goto((40, 25))
        self.pen2.goto((95, 20))
        self.pen2.goto((80, 20))
        self.pen2.penup()
        self.pen2.goto((60, 20))
        self.pen1.pendown()
        self.pen2.pendown()
        self.pen2.goto((45, 20))
        self.pen1.goto((40, -15))
        self.pen2.goto((45, -10))
        self.pen1.penup()
        self.pen2.penup()
        # l
        self.pen1.goto((120, -35))
        self.pen1.pendown()
        self.pen1.goto((140, -35))
        self.pen1.goto((140, 55))
        self.pen1.goto((120, 55))
        self.pen1.goto((120, -35))
        self.pen1.penup()
        # e
        self.pen1.color("red")
        self.pen2.color("red")
        self.pen1.goto((160, -35))
        self.pen1.pendown()
        self.pen1.goto((220, -35))
        self.pen1.goto((220, -25))
        self.pen1.goto((180, -25))
        self.pen1.goto((180, -5))
        self.pen1.goto((220, -5))
        self.pen1.goto((220, 25))
        self.pen1.goto((160, 25))
        self.pen1.goto((160, -35))
        self.pen1.penup()
        self.pen2.goto((180, 5))
        self.pen2.pendown()
        self.pen2.goto((200, 5))
        self.pen2.goto((200, 15))
        self.pen2.goto((180, 15))
        self.pen2.goto((180, 5))
        self.pen2.penup()



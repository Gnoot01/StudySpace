from turtle import Turtle

class Walls():

    def __init__(self):
        self.edges_coords = [# Top half
                             (-280, 5), (-240, 5), (-240, 25), (-280, 25), (-280, 75), (280, 75), (280, 25), (240, 25),
                             (240, 5), (280, 5),
                             # Bottom half
                             (280, -15), (240, -15), (240, -35), (280, -35), (280, -85),
                             # Obstacle 1 R->L
                             (100, -85), (100, -65), (90, -65), (90, -85),
                             # Obstacle 2
                             (50, -85), (50, -65), (40, -65), (40, -85),
                             # Obstacle 3
                             (-90, -85), (-90, -55), (-100, -55), (-100, -85),
                             # Continuing bottom half
                             (-280, -85), (-280, -35), (-240, -35), (-240, -15), (-280, -15),
                             # Top half obstacles
                             (-260, 55), (-240, 55), (-240, 45), (-260, 45), (-260, 55), (-120, 55), (20, 55), (20, 45),
                             (-120, 45), (-120, 55), (50, 55), (100, 55), (100, 45), (50, 45), (50, 55), (160, 55),
                             (200, 55), (200, 45), (160, 45), (160, 55), (220, 55),
                             # Bottom half obstacles
                             (260, 55), (260, 45), (220, 45), (220, 55), (-260, -55), (-230, -55), (-230, -65),
                             (-260, -65), (-260, -55), (-210, -55), (-120, -55), (-120, -65), (-210, -65), (-210, -55),
                             (-70, -55),
                             # T obstacle
                             (20, -55), (20, -65), (-70, -65), (-70, -55), (40, -35),
                             # The rest
                             (100, -35), (100, -45), (75, -45), (75, -65), (65, -65), (65, -45), (40, -45), (40, -35),
                             (120, -55), (200, -55), (200, -65), (120, -65), (120, -55), (220, -55),
                             # G
                             (260, -55), (260, -65), (220, -65), (220, -55),
                             # o
                             (-220, 55), (-140, 55), (-140, 35), (-200, 35), (-200, -15), (-160, -15), (-160, 5),
                             (-180, 5), (-180, 15), (-140, 15), (-140, -35), (-220, -35), (-220, 55), (-120, -35),
                             # o
                             (-60, -35), (-60, 25), (-120, 25), (-120, -35), (-40, -35), (20, -35), (20, 25), (-40, 25),
                             (-40, -35),
                             # Ghost cage
                             (40, -15), (100, -15), (100, 25), (80, 25), (80, 25), (60, 25), (60, 20), (80, 20), (80, 25),
                             (60, 25), (40, 25), (40, -15),
                             # l
                             (120, -35), (140, -35), (140, 55), (120, 55), (120, -35),
                             # e
                             (160, -35), (220, -35), (220, -25), (180, -25), (180, -5), (220, -5),(220, 25), (160, 25),
                             (160, -35)]
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
        # Continuing bottom half
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
        # The rest
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



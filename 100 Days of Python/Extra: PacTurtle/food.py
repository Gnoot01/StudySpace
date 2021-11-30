from turtle import Turtle
import time

class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.NORMAL_LOCATIONS = [# layer 1
                                 (-270, 65), (-260, 65), (-250, 65), (-240, 65), (-230, 65), (-220, 65), (-210, 65), (-200, 65), (-190, 65),  (-180, 65), (-170, 65), (-160, 65), (-150, 65), (-140, 65), (-130, 65), (-120, 65), (-110, 65), (-100, 65), (-90, 65), (-80, 65), (-70, 65), (-60, 65), (-50, 65), (-40, 65), (-30, 65), (-20, 65), (-10, 65), (0, 65), (10, 65), (20, 65), (30, 65), (40, 65), (50, 65), (60, 65), (70, 65), (80, 65), (90, 65), (100, 65), (110, 65), (120, 65), (130, 65), (140, 65), (150, 65), (160, 65), (170, 65), (180, 65), (190, 65), (200, 65), (210, 65), (220, 65), (230, 65), (240, 65), (250, 65), (260, 65), (270, 65),
                                 # layer 2
                                 (-270, 55),
                                 (-230, 55),
                                 (-130, 55),
                                 (30, 55),
                                 (150, 55),
                                 (210, 55),
                                 (270, 55),
                                 # layer 3
                                 (-230, 45),
                                 (-130, 45),
                                 (30, 45),
                                 (150, 45),
                                 (210, 45),
                                 # layer 4
                                 (-270, 35), (-260, 35), (-250, 35), (-240, 35), (-230, 35),
                                 (-130, 35), (-120, 35), (-110, 35), (-100, 35), (-90, 35), (-80, 35), (-70, 35), (-60, 35), (-50, 35), (-40, 35), (-30, 35), (-20, 35), (-10, 35), (0, 35), (10, 35), (20, 35), (30, 35),
                                 (150, 35), (160, 35), (170, 35), (180, 35), (190, 35), (200, 35), (210, 35), (220, 35), (230, 35), (240, 35), (250, 35), (260, 35), (270, 35),
                                 # layer 5
                                 (-230, 25),
                                 (-190, 25), (-180, 25), (-170, 25), (-160, 25), (-150, 25), (-140, 25), (-130, 25),
                                 (-50, 25),
                                 (150, 25),
                                 (230, 25),
                                 # layer 6
                                 (-230, 15),
                                 (-190, 15),
                                 (-130, 15),
                                 (-50, 15),
                                 (150, 15),
                                 (230, 15),
                                 # layer 7
                                 (-230, 5),
                                 (-190, 5),
                                 (-130, 5),
                                 (-50, 5),
                                 (150, 5),
                                 (230, 5),
                                 # layer 8
                                 (-230, -5),
                                 (-190, -5), (-180, -5),
                                 (-130, -5),
                                 (-50, -5),
                                 (150, -5),
                                 (230, -5),
                                 # layer 9
                                 (-230, -15),
                                 (-130, -15),
                                 (-50, -15),
                                 (150, -15),
                                 (190, -15), (200, -15), (210, -15), (220, -15), (230, -15),
                                 # layer 10
                                 (-230, -25),
                                 (-130, -25),
                                 (-50, -25),
                                 (150, -25),
                                 (230, -25),
                                 # layer 11
                                 (-230, -35),
                                 (-130, -35),
                                 (-50, -35),
                                 (150, -35),
                                 (230, -35),
                                 # layer 12
                                 (-270, -45), (-260, -45), (-250, -45), (-240, -45), (-230, -45), (-220, -45), (-210, -45), (-200, -45), (-190, -45),  (-180, -45), (-170, -45), (-160, -45), (-150, -45), (-140, -45), (-130, -45), (-120, -45), (-110, -45), (-100, -45), (-90, -45), (-80, -45), (-70, -45), (-60, -45), (-50, -45), (-40, -45), (-30, -45), (-20, -45), (-10, -45), (0, -45), (10, -45), (20, -45), (30, -45),
                                 (110, -45), (120, -45), (130, -45), (140, -45), (150, -45), (160, -45), (170, -45), (180, -45), (190, -45), (200, -45), (210, -45), (220, -45), (230, -45), (240, -45), (250, -45), (260, -45), (270, -45),
                                 # layer 13
                                 (-270, -55), (-220, -55), (-110, -55), (-80, -55), (30, -55), (40, -55), (50, -55), (60, -55), (80, -55), (90, -55), (100, -55), (110, -55), (210, -55), (270, -55),
                                 # layer 14
                                 (-270, -65), (-220, -65), (-110, -65), (-80, -65), (30, -65), (60, -65), (80, -65), (110, -65), (210, -65), (270, -65),
                                 # layer 15 L->R
                                 (-260, -75), (-250, -75), (-240, -75), (-230, -75), (-220, -75), (-210, -75), (-200, -75), (-190, -75),  (-180, -75), (-170, -75), (-160, -75), (-150, -75), (-140, -75), (-130, -75), (-120, -75), (-110, -75),
                                 (-80, -75), (-70, -75), (-60, -75), (-50, -75), (-40, -75), (-30, -75), (-20, -75), (-10, -75), (0, -75), (10, -75), (20, -75), (30, -75),
                                 (60, -75), (70, -75), (80, -75),
                                 (110, -75), (120, -75), (130, -75), (140, -75), (150, -75), (160, -75), (170, -75), (180, -75), (190, -75), (200, -75), (210, -75), (220, -75), (230, -75), (240, -75), (250, -75), (260, -75)]
        self.POWERUP_LOCATIONS = [# layer 3
                                  (-270, 45), (270, 45),
                                  # layer 8
                                  (-170, -5),
                                  # layer 15
                                  (-270, -75), (270, -75)]
        self.CHERRY_LOCATIONS = [(70, -25)]
        self.hideturtle()
        self.penup()
        self.update_food()


    def update_food(self):
        self.clear()
        self.setup_normal()
        self.setup_powerup()
        # How to get cherry to display only after 20s timed?
        self.setup_cherry()

    def setup_normal(self):
        for location in self.NORMAL_LOCATIONS:
            self.goto(location)
            self.dot(4, "pink")

    def setup_powerup(self):
        for location in self.POWERUP_LOCATIONS:
            self.goto(location)
            self.dot(8, "pink")

    def setup_cherry(self):
        for location in self.CHERRY_LOCATIONS:
            self.goto(location)
            self.dot(9, "red")

    def remove(self, location):
        for whichever in self.NORMAL_LOCATIONS, self.POWERUP_LOCATIONS, self.CHERRY_LOCATIONS:
            if location in whichever:
                whichever.remove(location)
        self.update_food()

from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager():
    def __init__(self):
        self.all_cars = []
        # car speed is 5 backwards or -5 forwards
        self.car_speed = STARTING_MOVE_DISTANCE

    def create(self):
        # Creates a car every screen.update aka 0.1s intervals. But we want less. so instead, we want to create a car
        # on average every 0.3s. TAKE NOTE! to regulate frequency
        random_chance = random.randint(1, 3)
        if random_chance == 1:
            car = Turtle("square")
            car.shapesize(stretch_len=2)
            car.color(random.choice(COLORS))
            car.penup()
            car.goto(300, random.randint(-210, 270))
            self.all_cars.append(car)
            self.move()

    def move(self):
        for car in self.all_cars:
            car.backward(self.car_speed)
            # VS
            # car.goto(car.xcor()-STARTING_MOVE_DISTANCE-move_increment, car.ycor())
            # .goto means doesn't increase speed, simply teleports move_increment/MOVE_INCREMENT distance away
            # we want to increase speed instead, so need to chance STARTING_MVOE_DISTANCE

    def upgrade_cars(self):
        self.car_speed += MOVE_INCREMENT
        # VS
        # self.move(MOVE_INCREMENT)


